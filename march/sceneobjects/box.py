from sceneobject import SceneObject
from ..vector3 import Vector3

class Box(SceneObject):
    def __init__(self, position, dimensions):
        self.position = position
        self.dimensions = dimensions/2

    def distance(self, point):
        return Vector3.max(
            abs(point - self.position) - self.dimensions,
            Vector3()
        ).length
