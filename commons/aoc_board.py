class Grid:

    def __init__(self):
        self.grid = {}
        self.dimensionality = None

    def get(self, point, default_value):
        return self[point] if point in self else default_value

    def items(self):
        return self.grid.items()

    def area(self):
        width = max(self.xs()) - min(self.xs())
        height = max(self.ys()) - min(self.ys())
        return width * height

    def reflect(self):
        result = Grid()
        for point, value in self.grid.items():
            result[point.reflect()] = value
        return result

    def rotate(self):
        result = Grid()
        for point, value in self.grid.items():
            result[point.rotate()] = value
        return result

    def xs(self):
        return set([point.x() for point in self.grid])

    def ys(self):
        if self.dimensionality < 2:
            return None
        return set([point.y() for point in self.grid])

    def __setitem__(self, point, value):
        if self.dimensionality is None:
            self.dimensionality = point.dimensions()
        self.grid[point] = value

    def __getitem__(self, point):
        return self.grid.get(point, None)

    def __contains__(self, point):
        return point in self.grid

    def __repr__(self):
        return str(self)

    def __str__(self):
        ys = self.ys()
        if ys is None:
            return self.make_row()
        if len(ys) == 0:
            return ''

        rows = []
        for y in range(min(ys), max(ys) + 1):
            rows.append(self.make_row(y))
        return '\n'.join(rows)

    def make_row(self, y=None):
        row, xs = [], self.xs()
        for x in range(min(xs), max(xs) + 1):
            point = Point(x, y) if y is not None else Point(x)
            value = str(self[point]) if point in self else '.'
            row.append(value) 
        return ''.join(row)


class Point:

    def __init__(self, *coords):
        self.coords = coords

    def dimensions(self):
        return len(self.coords)

    def x(self):
        return self.__get_coord(0)

    def y(self):
        return self.__get_coord(1)

    def z(self):
        return self.__get_coord(2)

    def reflect(self):
        return Point(-self.coords[0], self.coords[1])

    def rotate(self):
        return Point(-self.coords[1], self.coords[0])

    def adjacent(self):
        adjacent = []
        for i in range(len(self.coords)):
            adjacent.append(self.__create_point(i, -1))
            adjacent.append(self.__create_point(i, 1))
        return adjacent

    def all_adjacent(self):
        adjacent = [self]
        for i in range(len(self.coords)):
            to_add = []
            for point in adjacent:
                to_add.append(point.__create_point(i, -1))
                to_add.append(point.__create_point(i, 1))
            adjacent.extend(to_add)
        return adjacent[1:]

    def right(self):
        return self.__create_point(0, 1)

    def left(self):
        return self.__create_point(0, -1)

    def up(self):
        return self.__create_point(1, 1)

    def down(self):
        return self.__create_point(1, -1)

    def validate(self, o):
        if len(self.coords) != len(o.coords):
            raise Exception('Cannot compare points of different dimensionality')

    def __len__(self):
        return sum([abs(c) for c in self.coords])

    def __add__(self, o):
        coords = []
        for c1, c2 in self.__zip_points(o):
            coords.append(c1 + c2)
        return Point(*coords)

    def __sub__(self, o):
        coords = []
        for c1, c2 in self.__zip_points(o):
            coords.append(c1 - c2)
        return Point(*coords)

    def __mul__(self, o):
        coords = []
        for c in self.coords:
            coords.append(o * c)
        return Point(*coords)

    def __rmul__(self, o):
        return self.__mul__(o)

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, o):
        matches = []
        for c1, c2 in self.__zip_points(o):
            matches.append(c1 < c2)
        return all(matches)

    def __le__(self, o):
        matches = []
        for c1, c2 in self.__zip_points(o):
            matches.append(c1 <= c2)
        return all(matches)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.coords)

    def __get_coord(self, i):
        return self.coords[i]

    def __create_point(self, i, amount):
        coords = list(self.coords)
        coords[i] += amount
        return Point(*coords)

    def __zip_points(self, o):
        self.validate(o)
        return zip(self.coords, o.coords)
