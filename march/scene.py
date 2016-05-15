from sceneobjects import *
from vector3 import Vector3

MAX_STEPS = 64
NEAR_PLANE = 0.5
EPSILON = 0.01
PIXEL_DIST = 0.01

class Scene:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        self.camera = Vector3()

        self.setup_test()

    def setup_test(self):
        self.camera = Vector3()
        self.objects.append(Sphere(Vector3(0, 0, 10), 3))
        self.objects.append(Box(Vector3(0, -3, 10), Vector3(100, 1, 100)))

    def render(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                cam_x = (x - self.width/2) * PIXEL_DIST
                cam_y = (self.height/2 - y) * PIXEL_DIST
                direction = (Vector3(cam_x, cam_y, NEAR_PLANE) - self.camera)\
                    .normalized()

                yield x, y, self.march(self.camera, direction)

    def march(self, origin, direction):
        t = 0

        for i in xrange(MAX_STEPS):
            closest = min(obj.distance(origin + direction*t)
                for obj in self.objects)

            if closest < EPSILON:
                return tuple(((MAX_STEPS - i) * c)/MAX_STEPS
                    for c in (255, 255, 255))

            t += closest

        return (0, 100, 0)
