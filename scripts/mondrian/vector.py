class Vector:
    """ A lightweight vector class in two-dimensions. """

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, lam):
        """ Multiply the vector by a scalar, lam. """
        return Vector(lam * self.x, lam * self.y)

    def __rmul__(self, lam):
        return self.__mul__(lam)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not self == other

    def __hash__(self):
        """ To keep Vector hashable when we define __eq__, define __hash__. """
        return self.x, self.y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def dot(self, other):
        """ Dot product, a.b = ax.bx + ay.by. """
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        """ z-component of vector cross product, a x b = ax.by - ay.bx. """
        return self.x * other.y - self.y * other.x