from sceneobject import SceneObject

class Sphere(SceneObject):
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def distance(self, point):
        return self.position.distance(point) - self.radius
