class Grid:

    def __init__(self):
        self.grid = {}

    def add(self, point, value):
        self.grid[point] = value

    def area(self):
        width = max(self.xs()) - min(self.xs())
        height = max(self.ys()) - min(self.ys())
        return width * height

    def xs(self):
        return [point.x for point in self.grid]

    def ys(self):
        return [point.y for point in self.grid]

    def distance(self, start, end, seen):
        queue = [(start, 0)]
        current = (None, None)

        while len(queue) > 0 and current[0] != end:
            current = queue.pop(0)
            for adjacent in self.adjacent(current[0], seen):
                queue.append((adjacent, current[1] + 1))
                seen.add(adjacent)            

        return current[1] if current[0] == end else None

    def adjacent(self, position, seen=None):
        if seen is None:
            seen = set()

        result = []
        for adjacent in position.adjacent():
            if str(self[adjacent]) == '.' and adjacent not in seen:
                result.append(adjacent)
        return result

    def __getitem__(self, position):
        return self.grid.get(position, None)

    def __contains__(self, position):
        return position in self.grid

    def __repr__(self):
        return str(self)

    def __str__(self):

        xs, ys = self.xs(), self.ys()

        rows = []
        for y in range(min(ys), max(ys) + 1):
            row = []
            for x in range(min(xs), max(xs) + 1):
                point = Point(x, y)
                value = self.grid[point]
                row.append(str(value))                
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

