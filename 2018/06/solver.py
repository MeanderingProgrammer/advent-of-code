import math
from collections import defaultdict

from commons.aoc_parser import Parser
from commons.aoc_board import Point


class PointGrid:

    def __init__(self, points):
        self.points = points

        xs = self.get_coord(lambda point: point.x())
        self.min_x = min(xs)
        self.max_x = max(xs)

        ys = self.get_coord(lambda point: point.y())
        self.min_y = min(ys)
        self.max_y = max(ys)

    def largest_finite(self):
        point_to_closest = defaultdict(set)
        for point in self.point_generator(0):
            single_closest = self.get_single_closest_point(point)
            if single_closest is not None:
                point_to_closest[single_closest].add(point)

        infinite_points = self.get_infinte(point_to_closest)

        finite_sizes = set()
        for point, closest in point_to_closest.items():
            if point not in infinite_points:
                finite_sizes.add(len(closest))

        return max(finite_sizes)

    def get_single_closest_point(self, point):
        distances = self.get_distances(point)
        min_distance = min(distances.values())

        closest_points = []
        for option, distance in distances.items():
            if distance == min_distance:
                closest_points.append(option)

        return closest_points[0] if len(closest_points) == 1 else None

    def get_infinte(self, point_to_closest):
        infinite = set()
        for point, closest in point_to_closest.items():
            for closest_point in closest:
                if self.on_boarder(closest_point):
                    infinite.add(point)
        return infinite

    def on_boarder(self, point):
        return point.x() in [self.min_x, self.max_x] or point.y() in [self.min_y, self.max_y]

    def within_max_distance(self, max_distance):
        within = 0
        offset = math.ceil(max_distance / len(self.points))
        for point in self.point_generator(offset):
            distances = self.get_distances(point)
            total_distance = sum(distances.values())
            if total_distance < max_distance:
                within += 1
        return within

    def get_distances(self, end):
        distances = {}
        for start in self.points:
            distances[start] = len(start - end)
        return distances

    def point_generator(self, offset):
        for x in range(self.min_x - offset, self.max_x + offset + 1):
            for y in range(self.min_y - offset, self.max_y + offset + 1):
                yield Point(x, y)

    def get_coord(self, f):
        return [f(point) for point in self.points]


def main():
    point_grid = get_point_grid()
    # Part 1: 3251
    print('Part 1: {}'.format(point_grid.largest_finite()))
    # Part 2: 47841
    print('Part 2: {}'.format(point_grid.within_max_distance(10_000)))


def get_point_grid():
    points = set()
    for line in Parser().lines():
        parts = line.split(', ')
        point = Point(int(parts[0]), int(parts[1]))
        points.add(point)
    return PointGrid(points)


if __name__ == '__main__':
    main()
