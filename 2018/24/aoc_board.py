class Grid:

    def __init__(self):
        self.grid = {}

    def area(self):
        width = max(self.xs()) - min(self.xs())
        height = max(self.ys()) - min(self.ys())
        return width * height

    def xs(self):
        return [point.x for point in self.grid]

    def ys(self):
        return [point.y for point in self.grid]

    def __setitem__(self, point, value):
        self.grid[point] = value

    def __getitem__(self, point):
        return self.grid.get(point, None)

    def __contains__(self, point):
        return point in self.grid

    def __repr__(self):
        return str(self)

    def __str__(self):
        xs, ys = self.xs(), self.ys()

        if len(xs) == 0 or len(ys) == 0:
            return ''

        rows = []
        for y in range(min(ys), max(ys) + 1):
            row = []
            for x in range(min(xs), max(xs) + 1):
                point = Point(x, y)
                value = str(self[point]) if point in self else '.'
                row.append(value)                
            rows.append(''.join(row))

        return '\n'.join(rows)


class Point:

    def __init__(self, *coords):
        self.coords = coords

    def adjacent(self):
        adjacent = []

        for i in range(len(self.coords)):
            coords_c1 = list(self.coords)
            coords_c1[i] -= 1
            adjacent.append(Point(*coords_c1))

            coords_c2 = list(self.coords)
            coords_c2[i] += 1
            adjacent.append(Point(*coords_c2))

        return adjacent

    def validate(self, o):
        if len(self.coords) != len(o.coords):
            raise Exception('Cannot compare points of different dimensionality')

    def __len__(self):
        return sum([abs(c) for c in self.coords])

    def __add__(self, o):
        self.validate(o)
        coords = []
        for c1, c2 in zip(self.coords, o.coords):
            coords.append(c1 + c2)
        return Point(*coords)

    def __sub__(self, o):
        self.validate(o)
        coords = []
        for c1, c2 in zip(self.coords, o.coords):
            coords.append(c1 + c2)
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
        self.validate(o)
        matches = []
        for c1, c2 in zip(self.coords, o.coords):
            matches.append(c1 < c2)
        return all(matches)

    def __le__(self, o):
        self.validate(o)
        matches = []
        for c1, c2 in zip(self.coords, o.coords):
            matches.append(c1 <= c2)
        return all(matches)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.coords)

