from .line import Line

class Polygon:
    """ A small class to represent a polygon in two dimensions. """

    def __init__(self, vertices):
        """
        Define the polygon from an ordered sequence of vertices and get its
        area and edges (as Line objects).

        """

        self.vertices = vertices
        self.n = len(self.vertices)
        self.area = self.get_area()
        self.edges = self.get_edges()

    def get_area(self):
        """ Calculate and return the area of the polygon."""

        # We use the "shoelace" algorithm to calculate the area, since the
        # polygon has no holes or self-intersections.
        s1 = s2 = 0
        for i in range(self.n):
            j = (i+1) % self.n
            s1 += self.vertices[i].x * self.vertices[j].y
            s2 += self.vertices[i].y * self.vertices[j].x
        return abs(s1 - s2) / 2

    def get_edges(self):
        """
        Determine an ordered sequence of edges for the polygon from its
        vertices as a list of Line objects.

        """

        edges = []
        # Indexes of edge endpoints in self.vertices: (0,1), (1,2), ...,
        # (n-2, n-1), (n-1, 0)
        vertex_pair_indices = [(i,(i+1) % self.n) for i in range(self.n)]
        for (i1, i2) in vertex_pair_indices:
            v1, v2 = self.vertices[i1], self.vertices[i2]
            edges.append(Line.from_endpoints(v1, v2))
        return edges

    def split(self, intersections):
        """ Return the two polygons created by splitting this polygon.

        Split the polygon into two polygons at the points given by
        intersections = (i1, p1), (i2, p2)
        where each tuple contains the index of an edge, i, intersected at the
        point, p, by a new line.

        Returns: a list of the new Polygon objects formed.

        """

        (i1, p1), (i2, p2) = intersections
        vertices1 = ([edge.p + edge.r for edge in self.edges[:i1]] +
                     [p1, p2] +
                     [edge.p + edge.r for edge in self.edges[i2:]])
        polygon1 = Polygon(vertices1)
        vertices2 = ([edge.p + edge.r for edge in self.edges[i1:i2]] +
                     [p2, p1])
        polygon2 = Polygon(vertices2)
        return [polygon1, polygon2]

    def __str__(self):
        return ', '.join([str(v) for v in self.vertices])