class Grid:

    def __init__(self):
        self.__grid = {}
        self.__dimensionality = None

    def get(self, point, default_value):
        return self[point] if point in self else default_value

    def items(self):
        return self.__grid.items()

    def area(self):
        width = max(self.xs()) - min(self.xs())
        height = max(self.ys()) - min(self.ys())
        return width * height

    def reflect(self):
        result = Grid()
        for point, value in self.items():
            result[point.reflect()] = value
        return result

    def rotate(self):
        result = Grid()
        for point, value in self.items():
            result[point.rotate()] = value
        return result

    def xs(self):
        return set([point.x() for point in self.__grid])

    def ys(self):
        if self.__dimensionality < 2:
            return None
        return set([point.y() for point in self.__grid])

    def __setitem__(self, point, value):
        if self.__dimensionality is None:
            self.__dimensionality = point.dimensions()
        elif self.__dimensionality != point.dimensions():
            raise Exception('Cannot create grid with mismatching dimensions')
        self.__grid[point] = value

    def __getitem__(self, point):
        return self.__grid.get(point, None)

    def __contains__(self, point):
        return point in self.__grid

    def __repr__(self):
        return str(self)

    def __str__(self):
        ys = self.ys()
        if ys is None:
            return self.__make_row()
        if len(ys) == 0:
            return ''

        rows = []
        for y in range(min(ys), max(ys) + 1):
            rows.append(self.__make_row(y))
        return '\n'.join(rows)

    def __make_row(self, y=None):
        row, xs = [], self.xs()
        for x in range(min(xs), max(xs) + 1):
            point = Point(x) if y is None else Point(x, y)
            value = str(self[point]) if point in self else '.'
            row.append(value) 
        return ''.join(row)


class Point:

    def __init__(self, *coords):
        self.__coords = coords

    # Basic Getters

    def dimensions(self):
        return len(self.__coords)

    def x(self):
        return self.__get(0)

    def y(self):
        return self.__get(1)

    def z(self):
        return self.__get(2)

    def __get(self, i):
        return self.__coords[i]

    # 2D Transformers

    def reflect(self):
        self.__verify_2d()
        return Point(-self.__get(0), self.__get(1))

    def rotate(self):
        self.__verify_2d()
        return Point(-self.__get(1), self.__get(0))

    def __verify_2d(self):
        if self.dimensions() != 2:
            raise Exception('This function only works on 2D points')

    # Get Adjacent points (either includes diagonals or not)

    def adjacent(self, diagonal=False):
        adjacent = [self] if diagonal else []
        for i in range(self.dimensions()):
            to_add = []
            to_modify = adjacent if diagonal else [self]

            for point in to_modify:
                to_add.append(point.__create(i, -1))
                to_add.append(point.__create(i, 1))

            adjacent.extend(to_add)

        return adjacent[1:] if diagonal else adjacent

    # Some Simple Directions (up increases y, careful when reading top to bottom)

    def right(self):
        return self.__create(0, 1)

    def left(self):
        return self.__create(0, -1)

    def up(self):
        return self.__create(1, 1)

    def down(self):
        return self.__create(1, -1)

    def __create(self, i, amount):
        coords = list(self.__coords)
        coords[i] += amount
        return Point(*coords)

    def validate(self, o):
        if self.dimensions() != o.dimensions():
            raise Exception('Cannot compare points of different dimensionality')

    def __len__(self):
        return sum([abs(coord) for coord in self.__coords])

    # Math Operations Between Points

    def __add__(self, o):
        return self.__math(o, lambda coord_1, coord_2: coord_1 + coord_2)

    def __sub__(self, o):
        return self.__math(o, lambda coord_1, coord_2: coord_1 - coord_2)

    def __math(self, o, f):
        self.validate(o)
        coords = []
        for coord_1, coord_2 in zip(self.__coords, o.__coords):
            coords.append(f(coord_1, coord_2))
        return Point(*coords)

    # Math Operations Between Point and Scalar

    def __mul__(self, amount):
        coords = []
        for coord in self.__coords:
            coords.append(coord * amount)
        return Point(*coords)

    def __rmul__(self, amount):
        return self.__mul__(amount)

    # Equality checks start from highest dimension

    def __lt__(self, o):
        comparison = self.__compare(o, lambda coord_1, coord_2: coord_1 < coord_2)
        return False if comparison is None else comparison

    def __le__(self, o):
        comparison = self.__compare(o, lambda coord_1, coord_2: coord_1 < coord_2)
        return True if comparison is None else comparison

    def __compare(self, o, f):
        self.validate(o)
        zipped = list(zip(self.__coords, o.__coords))
        zipped.reverse()
        for coord_1, coord_2 in zipped:
            if coord_1 != coord_2:
                return f(coord_1, coord_2)
        return None

    # Basic Equality, Hash, and to String implementations

    def __eq__(self, o):
        return isinstance(o, Point) and self.__coords == o.__coords

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__coords)
