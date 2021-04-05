from collections import defaultdict

from aoc_parser import Parser


FILE_NAME = 'data'


class Action:

    def __init__(self, value):
        self.value = value

    def apply(self, current, v2):
        return self.apply_v2(current) if v2 else self.apply_v1(current)

    def apply_v1(self, current):
        if self.value == 'turn on':
            return 1
        elif self.value == 'turn off':
            return 0
        elif self.value == 'toggle':
            return 1 - current
        else:
            raise Exception('Unknown state changer: {}'.format(self.value))

    def apply_v2(self, current):
        if self.value == 'turn on':
            return current + 1
        elif self.value == 'turn off':
            return max(current - 1, 0)
        elif self.value == 'toggle':
            return current + 2
        else:
            raise Exception('Unknown state changer: {}'.format(self.value))


class PointRange:

    def __init__(self, value):
        bottom_left = self.to_point(value[0])
        top_right = self.to_point(value[2])
        self.points = self.to_points(bottom_left, top_right)

    @staticmethod
    def to_point(coords):
        return [int(coord) for coord in coords.split(',')]

    @staticmethod
    def to_points(bottom_left, top_right):
        points = set()
        for x in range(bottom_left[0], top_right[0] + 1):
            for y in range(bottom_left[1], top_right[1] + 1):
                points.add((x, y))
        return points


class Direction:

    def __init__(self, value):
        value = value.split()
        self.action = Action(' '.join(value[:-3]))
        self.point_range = PointRange(value[-3:])

    def apply(self, grid, v2):
        for point in self.point_range.points:
            grid[point] = self.action.apply(grid[point], v2)


def main():
    directions = get_directions()
    # Part 1: 400410
    print('Part 1: {}'.format(run_grid(directions, False)))
    # Part 2: 15343601
    print('Part 2: {}'.format(run_grid(directions, True)))


def run_grid(directions, v2):
    grid = defaultdict(int)
    for direction in directions:
        direction.apply(grid, v2)
    return sum(grid.values())


def get_directions():
    return [Direction(line) for line in Parser(FILE_NAME).lines()]


if __name__ == '__main__':
    main()
