class Grid:

    def __init__(self):
        self.grid = {}

    def add(self, point, value):
        if point not in self.grid:
            self.grid[point] = []
        self.grid[point].append(value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.grid)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(
            self.x + o.x,
            self.y + o.y
        )

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
