from .constants import EPS

class Line:
    """ A simple class representing a line segment between two points in 2D. """

    def __init__(self, p, r):
        """
        p is the start point vector, r is the vector from this start point
        to the end point.

        """

        self.p, self.r = p, r

    @classmethod
    def from_endpoints(self, p, q):
        """ Create and return the Line object between points p and q. """

        return Line(p, q - p)

    def __str__(self):
        return '{} -> {}'.format(self.p, (self.p + self.r))

    def intersection(self, other):
        """
        Return the vector to the intersection point between two line segments
        self and other, or None if the lines do not intersect.

        """

        p, r = self.p, self.r
        q, s = other.p, other.r

        rxs = r.cross(s)
        if rxs == 0:
            # Line segments are parallel: no intersection
            return None
        u = (q - p).cross(r) / rxs
        t = (q - p).cross(s) / rxs

        if -EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS:
            # We have an intersection!
            return p + t * r

        # Line segments are not parallel but don't intersect
        return None

    def get_point_on_line(self, u):
        """ Return the vector to the point on the line defined by p + ur. """
        return self.p + u * self.r

    def is_parallel(self, other):
        """ Are the lines self and other parallel? """

        return abs(self.r.cross(other.r)) < EPS

    def is_colinear(self, other):
        """
        Are the lines colinear (have the same start and end points, in either
        order)? """

        return (self.is_parallel(other) and
                abs((self.p - other.p).cross(self.r)) < EPS)