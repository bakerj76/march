import pygame
import random
import time
from scene import Scene

class March:
    def __init__(self, width, height, scale=1):
        self.width = width
        self.height = height
        self.scale = scale
        self.running = False

    @property
    def real_width(self):
        return self.width * self.scale

    @property
    def real_height(self):
        return self.height * self.scale

    def start(self):
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((self.real_width,
            self.real_height))
        self.surface = pygame.Surface((self.width, self.height))

        self.draw()

        while self.running:
            self.handle_events()

        self.quit()

    def draw(self):
        self.render()
        scaled_surface = pygame.transform.scale(self.surface,
            (self.real_width, self.real_height))

        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def render(self):
        scene = Scene(self.width, self.height)

        start = time.time()

        for x, y, pixel in scene.render():
            self.surface.set_at((x, y), pixel)

        end = time.time()
        print('Rendered in {0}s'.format(end - start))

    def quit(self):
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        e = pygame.event.poll()

        if e.type == pygame.QUIT:
            self.running = False
