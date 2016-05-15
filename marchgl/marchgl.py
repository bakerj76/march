import ctypes
import numpy
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import os
import pygame
from pygame.locals import *

from vector3 import Vector3

SCRIPT_DIR = os.path.dirname(__file__)
RAY_VERT_FILE = os.path.join(SCRIPT_DIR, r'shaders/raymarch.vs')
RAY_FRAG_FILE = os.path.join(SCRIPT_DIR, r'shaders/raymarch.fs')

STD_VERT_FILE = os.path.join(SCRIPT_DIR, r'shaders/standard.vs')
STD_FRAG_FILE = os.path.join(SCRIPT_DIR, r'shaders/standard.fs')

class March:
    def __init__(self, width, height, scale=1):
        self.width = width
        self.height = height
        self.scale = scale
        self.running = False

        self.ray_shader = None
        self.std_shader = None
        self.draw_texture = None
        self.vbo = None
        self.ebo = None
        self.fbo = None

        self.camera = Vector3()
        self.uniforms = {}

        self.clock = pygame.time.Clock()

    @property
    def real_width(self):
        return self.width * self.scale

    @property
    def real_height(self):
        return self.height * self.scale

    def start(self):
        self.running = True
        pygame.init()

        pygame.display.set_caption("Awww yeah")
        self.screen = pygame.display.set_mode(
            (self.real_width, self.real_height),
            HWSURFACE | OPENGL | DOUBLEBUF
        )

        glClearColor(0, 0, 0, 1)
        self.reload()

        while self.running:
            self.handle_events()
            self.draw()

        self.quit()

    def reload(self):
        with open(RAY_VERT_FILE) as vert, open(RAY_FRAG_FILE) as frag:
            self.ray_shader = self.create_shader(vert.read(), frag.read())

        with open(STD_VERT_FILE) as vert, open(STD_FRAG_FILE) as frag:
            self.std_shader = self.create_shader(vert.read(), frag.read())

        self.setup(self.ray_shader, self.std_shader)
        self.setup_uniforms()

    def setup_uniforms(self):
        glUseProgram(self.ray_shader)
        self.uniforms['cameraPos'] = glGetUniformLocation(self.ray_shader, 'cameraPos')

    def draw(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(self.ray_shader)
        self.set_uniforms()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.draw_texture)
        glDrawArrays(GL_QUADS, 0, 4)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, self.real_width, self.real_height)
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(self.std_shader)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.draw_texture)
        glDrawArrays(GL_QUADS, 0, 4)

        pygame.display.flip()
        self.clock.tick()
        print str(self.clock.get_fps()) + '\r',

    def set_uniforms(self):
        glUniform3f(self.uniforms['cameraPos'], *self.camera)

    def quit(self):
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        e = pygame.event.poll()

        if e.type == pygame.QUIT:
            self.running = False

        if e.type == pygame.KEYUP and e.key == pygame.K_RETURN:
            self.reload()
        elif pygame.key.get_pressed()[pygame.K_w]:
            self.camera.z += 5 * self.clock.get_time()/1000.0
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.camera.z -= 5 * self.clock.get_time()/1000.0


    def create_shader(self, vert, frag):
        return compileProgram(
            compileShader(vert, GL_VERTEX_SHADER),
            compileShader(frag, GL_FRAGMENT_SHADER)
        )

    def setup(self, ray_shader, std_shader):
        verts = numpy.array(
        #    verts    uv
            [-1,  1,  0,  1,
              1,  1,  1,  1,
              1, -1,  1,  0,
             -1, -1,  0,  0],
            dtype=numpy.float32)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 4*len(verts), verts, GL_STATIC_DRAW)


        position = glGetAttribLocation(ray_shader, 'position')
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 4*4, None)

        position = glGetAttribLocation(std_shader, 'position')
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 4*4, None)

        texcoord = glGetAttribLocation(std_shader, 'texcoord')
        glEnableVertexAttribArray(texcoord)
        glVertexAttribPointer(texcoord, 2, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(4*2))

        self.draw_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.draw_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0,
            GL_RGBA, GL_FLOAT, None)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
            GL_TEXTURE_2D, self.draw_texture, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise Exception('well... fuck.')
