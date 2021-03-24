class Grid:

    def __init__(self):
        self.grid = set()

    def add(self, point):
        self.grid.add(point)

    def area(self):
        width = max(self.xs()) - min(self.xs())
        height = max(self.ys()) - min(self.ys())
        return width * height

    def xs(self):
        return [point.x for point in self.grid]

    def ys(self):
        return [point.y for point in self.grid]

    def __contains__(self, item):
        return item in self.grid

    def __repr__(self):
        return str(self)

    def __str__(self):
        xs, ys = self.xs(), self.ys()

        rows = []
        for y in range(min(ys), max(ys) + 1):
            row = []
            for x in range(min(xs), max(xs) + 1):
                value = '#' if Point(x, y) in self.grid else '.'
                row.append(value)                
            rows.append(''.join(row))

        return '\n'.join(rows)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def adjacent(self):
        return [
            self.left(), self.right(),
            self.up(), self.down()
        ]

    def left(self):
        return Point(self.x - 1, self.y)

    def right(self):
        return Point(self.x + 1, self.y)

    def up(self):
        return Point(self.x, self.y - 1)

    def down(self):
        return Point(self.x, self.y + 1)

    def __len__(self):
        return abs(self.x) + abs(self.y)

    def __add__(self, o):
        return Point(
            self.x + o.x,
            self.y + o.y
        )

    def __sub__(self, o):
        return Point(
            self.x - o.x,
            self.y - o.y
        )

    def __mul__(self, o):
        return Point(
            self.x * o,
            self.y * o
        )

    def __rmul__(self, o):
        return self.__mul__(o)

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

