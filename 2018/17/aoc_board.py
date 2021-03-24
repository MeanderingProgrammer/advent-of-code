class Grid:

    def __init__(self):
        self.grid = {}

        self.min_x = None
        self.max_x = None

        self.min_y = None
        self.max_y = None

    def area(self):
        width = self.max_x - self.min_x
        height = self.max_y - self.min_y
        return width * height

    def in_range(self, point, use_min=True):
        y = point.y
        min_value = self.min_y if use_min else 1
        return y >= min_value and y <= self.max_y

    def update_bounds(self, point):
        x = point.x
        if self.min_x is None or x < self.min_x:
            self.min_x = x
        if self.max_x is None or x > self.max_x:
            self.max_x = x

        y = point.y
        if self.min_y is None or y < self.min_y:
            self.min_y = y
        if self.max_y is None or y > self.max_y:
            self.max_y = y

    def __setitem__(self, point, value):
        if value != '.':
            self.update_bounds(point)
        self.grid[point] = value

    def __getitem__(self, point):
        return self.grid.get(point, None)

    def __contains__(self, point):
        return point in self.grid

    def __repr__(self):
        return str(self)

    def __str__(self):
        rows = []
        for y in range(self.min_y, self.max_y + 1):
            row = []
            for x in range(self.min_x, self.max_x + 1):
                point = Point(x, y)
                value = str(self[point]) if point in self else '.'
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

    def __lt__(self, o):
        if self.y == o.y:
            return self.x < o.x
        return self.y < o.y

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

