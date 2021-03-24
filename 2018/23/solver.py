import math
from aoc_parser import Parser
from aoc_board import Grid, Point


FILE_NAME = 'data'


class NanoBot:

    def __init__(self, value):
        pos, radius = value.split(', ')
        self.pos = Point(*[int(c) for c in pos.split('=')[1][1:-1].split(',')])
        self.r = int(radius.split('=')[1])

    def in_range(self, o):
        diff = self.pos - o
        return len(diff) <= self.r

    def cube(self):
        coords = self.pos.coords
        return Cube(*[(c + self.r, c - self.r) for c in coords])

    def __lt__(self, o):
        return self.r < o.r

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}, {}'.format(self.pos, self.r)


def main():
    bots = get_bots()
    bots.sort()

    strongest_bot = bots[-1]

    # Part 1 = 383
    bots_in_range = [bot for bot in bots if strongest_bot.in_range(bot.pos)]
    print('Total bots in range = {}'.format(len(bots_in_range)))

    # Part 2 = 100474026
    bounds = get_bounds(bots)
    for i in range(10):
        best_value, best_bounds = 0, None
        x_bounds, y_bounds, z_bounds = split_bounds(bounds, 10)
        for x_bound in x_bounds:
            for y_bound in y_bounds:
                for z_bound in z_bounds:
                    value = approximate_value(x_bound, y_bound, z_bound, bots)
                    if value > best_value:
                        best_bounds = [x_bound, y_bound, z_bound]
                        best_value = value
        print(bounds)
        print(best_bounds)
        print(best_value)
        bounds = best_bounds


def get_bounds(bots):
    xs, ys, zs = [], [], []
    for bot in bots:
        coords = bot.pos.coords
        xs.append(coords[0])
        ys.append(coords[1])
        zs.append(coords[2])
    return [
        (min(xs), max(xs)),
        (min(ys), max(ys)),
        (min(zs), max(zs))
    ]


def split_bounds(bounds, value):
    step_sizes = [math.ceil((bound[1] - bound[0]) / value) for bound in bounds]
    x_bounds, y_bounds, z_bounds = [], [], []
    for i in range(value):
        bound_starts = [(bound[0] + (i * step_sizes[j])) for j, bound in enumerate(bounds)]
        bound_splits = [(bound_start, bound_start + step_sizes[j]) for j, bound_start in enumerate(bound_starts)]

        x_bounds.append(bound_splits[0])
        y_bounds.append(bound_splits[1])
        z_bounds.append(bound_splits[2])

    return x_bounds, y_bounds, z_bounds


def approximate_value(x_bound, y_bound, z_bound, bots):
    n = 20
    values = []
    for i in range(n + 1):
        test_position = Point(
            (((i) * x_bound[1]) + ((n - i) * x_bound[0])) // n,
            (((i) * y_bound[1]) + ((n - i) * y_bound[0])) // n,
            (((i) * z_bound[1]) + ((n - i) * z_bound[0])) // n
        )
        value = in_range_of_bots(test_position, bots)
        values.append(value)
    return max(values)


def binary_search(points, bots, start_value):
    if len(points) == 1:
        return points[0]

    mid = len(points) // 2
    point = points[mid]
    value = len(in_range_of_bots(point, bots))

    if value <= start_value:
        return binary_search(points[:mid], bots, start_value)
    else:
        return binary_search(points[mid:], bots, value)


def in_range_of_bots(pos, bots):
    return len([bot for bot in bots if bot.in_range(pos)])


def get_bots():
    bots = []
    for line in Parser(FILE_NAME).lines():
        bot = NanoBot(line)
        bots.append(bot)
    return bots


if __name__ == '__main__':
    main()
