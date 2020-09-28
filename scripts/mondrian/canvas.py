import random
import os
from .constants import EPS
from .line import Line
from .polygon import Polygon
from .vector import Vector

class Canvas:
    # Fill colours for polygons, and their cumulative probability distribution
    colours = ['blue', 'red', 'yellow', 'white']
    colours_cdf = [0.15, 0.3, 0.45, 1.0]

    def get_colour(self):
        """
        Pick a colour at random using the cumulative probability distribution
        colours_cdf.

        """

        cprob = random.random()
        i = 0
        while Canvas.colours_cdf[i] < cprob:
            i += 1
        return Canvas.colours[i]

    def __init__(self, width, height):
        """ Initialize the canvas with a border around the outside. """

        self.width, self.height = width, height
        self.lines = []

        corners = Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1, 0)
        self.add_line(Line(corners[0], Vector(0, 1)))
        self.add_line(Line(corners[1], Vector(1, 0)))
        self.add_line(Line(corners[2], Vector(0, -1)))
        self.add_line(Line(corners[3], Vector(-1, 0)))

        self.polygons = {Polygon(corners)}

    def add_line(self, new_line):
        """ Add new_line to the list of Line objects. """
        self.lines.append(new_line)

    def split_polygons(self, new_line):
        """
        Split any Polygons which are intersected exactly twice by new_line.

        Returns the set of "old" Polygons split and a list of the "new"
        Polygons thus formed.

        """
        new_polygons = []
        old_polygons = set()
        for polygon in self.polygons:
            intersections = []
            for i, edge in enumerate(polygon.edges):
                p = new_line.intersection(edge)
                if p:
                    intersections.append((i, p))
            if len(intersections) == 2:
                # this polygon is split into two by the new line
                new_polygons.extend(polygon.split(intersections))
                old_polygons.add(polygon)

        return old_polygons, new_polygons

    def update_polygons(self, old_polygons, new_polygons):
        """
        Update the set of Polygon objects by removing old_polygons and adding
        new_polygons to self.polygons.

        """

        self.polygons -= old_polygons
        self.polygons.update(new_polygons)

    def get_new_line(self):
        """ Return a random new line with endpoints on two existing lines. """

        # Get a random point on each of any two different existing lines.
        line1, line2 = random.sample(self.lines, 2)
        start = line1.get_point_on_line(random.random())
        end = line2.get_point_on_line(random.random())
        # Create and return a new line between the points
        return Line.from_endpoints(start, end)

        def get_xy(line):
            """ Return 'x' for horizontal line or 'y' for vertical line. """
            return 'x' if abs(line.r.y) < EPS else 'y'

        def get_other_xy(xy):
            """ Passed 'x' or 'y', return 'y' or 'x'. """
            return 'y' if xy == 'x' else 'x'

        # Is this a line in parallel to the x-axis or the y-axis?
        xy = get_xy(line1)
        other_xy = get_other_xy(xy)

        start = line1.get_point_on_line(random.random())
        c = getattr(start, xy)
        parallel_lines = []
        for line in self.lines:
            if line.is_colinear(line1):
                continue
            if get_xy(line) != xy:
                # This line is perpendicular to our choice
                continue
            c1, c2 = sorted([getattr(line.p, xy), getattr(line.p + line.r, xy)])
            if not c1 <= c <= c2:
                continue
            parallel_lines.append(line)
        line2 = random.choice(parallel_lines)

        end = Vector(None, None)
        setattr(end, xy, getattr(start, xy))
        setattr(end, other_xy, getattr(line2.p, other_xy))

        return Line.from_endpoints(start, end)

    def get_new_orthogonal_line(self):
        """
        Return a new horizontal or vertical line between two existing lines.

        """

        line1 = random.choice(self.lines)

        def get_xy(line):
            """ Return 'x' for horizontal line or 'y' for vertical line. """
            return 'x' if abs(line.r.y) < EPS else 'y'

        def get_other_xy(xy):
            """ Passed 'x' or 'y', return 'y' or 'x'. """
            return 'y' if xy == 'x' else 'x'

        # Is this a line in parallel to the x-axis or the y-axis?
        xy = get_xy(line1)
        other_xy = get_other_xy(xy)

        start = line1.get_point_on_line(random.random())
        c = getattr(start, xy)
        parallel_lines = []
        for line in self.lines:
            if line.is_colinear(line1):
                continue
            if get_xy(line) != xy:
                # This line is perpendicular to our choice
                continue
            c1, c2 = sorted([getattr(line.p, xy), getattr(line.p + line.r, xy)])
            if not c1 <= c <= c2:
                continue
            parallel_lines.append(line)
        line2 = random.choice(parallel_lines)

        end = Vector(None, None)
        setattr(end, xy, getattr(start, xy))
        setattr(end, other_xy, getattr(line2.p, other_xy))

        return Line.from_endpoints(start, end)

    def make_painting(self, nlines, minarea=None):
        """
        Make the "painting" by adding nlines randomly, such that no polygon
        is formed with an area less than minarea.

        """

        for i in range(nlines):
            while True:
                # Create a new line and split any polygons it intersects
                new_line = self.get_new_orthogonal_line()
                old_polygons, new_polygons = self.split_polygons(new_line)

                # If required, ensure that the smallest polygon is at least
                # minarea in area, and go back around if not
                if minarea:
                    smallest_polygon_area = min(polygon.area
                                                for polygon in new_polygons)
                    if smallest_polygon_area >= minarea:
                        break
                else:
                    break

            self.update_polygons(old_polygons, new_polygons)
            self.add_line(new_line)

    def get_svg(self):
        """ Write the image as an SVG file to filename. """
        svg = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        svg += f'width="{self.width}" height="{self.height}">'
        svg += '<defs>'
        svg += '<style type="text/css"><![CDATA[line {stroke: #000;stroke-width: 5px;fill: none;}]]></style></defs>'

        for polygon in self.polygons:
            path = []
            for vertex in polygon.vertices:
                path.append((vertex.x * self.width, vertex.y * self.height))
            s = 'M{},{} '.format(*path[0])
            s += ' '.join(['L{},{}'.format(*path[i])
                           for i in range(polygon.n)])
            colour = self.get_colour()
            svg += f'<path d="{s}" style="fill: {colour}"/>'

        for line in self.lines[4:]:
            x1, y1 = line.p.x * self.width, line.p.y * self.height
            x2, y2 = ((line.p + line.r).x * self.width,
                      (line.p + line.r).y * self.height)

            svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'

        svg += f'''<g fill="none" stroke="black"><path stroke-width="8"
                    d="M0,0l{self.width},0l0,{self.height}l-{self.width},0,l0,-{self.height}"/></g></svg>
        '''

        return svg
