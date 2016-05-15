import math

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        return self * scalar

    def __div__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __iter__(self):
        for n in (self.x, self.y, self.z):
            yield n

    @property
    def length(self):
        x, y, z = self.x, self.y, self.z
        return math.sqrt(x*x + y*y + z*z)

    def distance(self, other):
        return (self - other).length

    def normalized(self):
        length = self.length

        if length == 0:
            return Vector3()

        return Vector3(self.x/length, self.y/length, self.z/length)

    def dot(self, other):
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def cross(self, other):
        return Vector3(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x
        )

    @staticmethod
    def max(a, b):
        result = Vector3(max(a.x, b.x), max(a.y, b.y), max(a.z, b.z))
        return result
