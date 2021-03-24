import math


class Grid:

    def __init__(self):
        self.grid = set()

    def add(self, point):
        self.grid.add(point)

    def points_with_max_distance(self, max_distance):
        total = 0
        bounds = self.get_bounds(max_distance)
        for x in range(bounds[0], bounds[2] + 1):
            for y in range(bounds[1], bounds[3] + 1):
                point = Point(x, y)
                valid = self.within_distance(point, max_distance)
                if valid:
                    total += 1
        return total

    def get_bounds(self, max_distance):
        traversal = math.ceil(max_distance / len(self.grid))
        return (
            self.min_x() - traversal,
            self.min_y() - traversal,
            self.max_x() + traversal,
            self.max_y() + traversal
        )

    def within_distance(self, start, max_distance):
        total_distance = 0
        for end in self.grid:
            distance = len(start - end)
            total_distance += distance
            if total_distance >= max_distance:
                return False
        return True

    def closest_points(self):
        result = []
        for x in range(self.max_x() + 1):
            for y in range(self.max_y() + 1):
                point = Point(x, y)
                closest = self.closest_point(point)
                result.append((point, closest))
        return result

    def closest_point(self, start):
        distances = []
        for end in self.grid:
            distances.append((end, len(start - end)))

        distances.sort(key = lambda distance: distance[1])
        shortest_distance = distances[0][1]

        distances = [distance for distance in distances if distance[1] == shortest_distance]
        return [distance[0] for distance in distances]

    def max_x(self):
        return self.max_value(lambda point: point.x)

    def max_y(self):
        return self.max_value(lambda point: point.y)

    def min_x(self):
        return self.min_value(lambda point: point.x)

    def min_y(self):
        return self.min_value(lambda point: point.y)

    def max_value(self, f):
        values = []
        for point in self.grid:
            values.append(f(point))
        return max(values)

    def min_value(self, f):
        values = []
        for point in self.grid:
            values.append(f(point))
        return min(values)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.grid)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

