import math
from OpenGL.GL import *
import pygame

from vector3 import Vector3

class Camera:
    def __init__(self, width, height, pos=None, z_near=0.5, z_far=25, fov=90):
        self.width = width
        self.height = height
        self.position = pos if pos is not None else Vector3()
        self.z_near = z_near
        self.z_far = z_far
        self.fov = fov

        self.calculate_dist()

    def calculate_dist(self):
        self.ray_dist = self.z_near*math.tan(math.radians(self.fov)/2.0)

class BVH:
    def __init__(self, object):
        self.is_leaf = object is not None
        self.object = object
        self.a = None
        self.b = None

    def generate(self, objects):
        pass

class Scene:
    def __init__(self, width, height):
        self.camera = Camera(width, height)
        self.objects = []

    def setup_uniforms(self, ray_shader, uniforms):
        uniforms['cameraPos'] = glGetUniformLocation(ray_shader, 'cameraPos')
        uniforms['rayDist'] = glGetUniformLocation(ray_shader, 'rayDist')
        glUniform1f(uniforms['rayDist'], self.camera.ray_dist)

        uniforms['zNear'] = glGetUniformLocation(ray_shader, 'zNear')
        glUniform1f(uniforms['zNear'], self.camera.z_near)

        uniforms['zFar'] = glGetUniformLocation(ray_shader, 'zFar')
        glUniform1f(uniforms['zFar'], self.camera.z_far)

    def set_uniforms(self, uniforms):
        glUniform3f(uniforms['cameraPos'], *self.camera.position)

    def update(self, event, delta_time):
        if pygame.key.get_pressed()[pygame.K_w]:
            self.camera.position.z += 10 * delta_time
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.camera.position.z -= 10 * delta_time
