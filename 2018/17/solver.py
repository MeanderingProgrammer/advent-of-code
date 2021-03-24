from aoc_parser import Parser
from aoc_board import Grid, Point
import sys

sys.setrecursionlimit(10_000)


FILE_NAME = 'data'


class PointRange:

    def __init__(self, raw):
        parts = raw.split(', ')
        coord_range = {}
        for part in parts:
            part = part.split('=')
            coord_range[part[0]] = self.get_range(part[1])
        self.xs = coord_range['x']
        self.ys = coord_range['y']

    def get_points(self):
        points = []
        for x in self.xs:
            for y in self.ys:
                point = Point(x, y)
                points.append(point)
        return points

    @staticmethod
    def get_range(values):
        values = values.split('..')
        if len(values) == 1:
            return [
                int(values[0])
            ]
        elif len(values) == 2:
            return list(range(
                int(values[0]),
                int(values[1]) + 1
            ))
        else:
            raise Exception('Can not handle such a range')


CLAY = '#'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'


class GroundReservoir:

    def __init__(self, grid):
        self.grid = grid
        self.flowing = set()
        self.settled = set()

    def fill(self, point, direction=DOWN):
        if self.grid[point] == CLAY:
            return True

        self.flowing.add(point)

        down = point.down()
        if not self.grid[down] == CLAY:
            if down not in self.flowing and self.grid.in_range(down, False):
                self.fill(down)
            if down not in self.settled:
                return False

        left = point.left()
        right = point.right()

        left_filled = left not in self.flowing and self.fill(left, LEFT)
        right_filled = right not in self.flowing and self.fill(right, RIGHT)

        # All water at this 'level' has settled
        if direction == DOWN and left_filled and right_filled:
            self.settled.add(point)
            while left in self.flowing:
                self.settled.add(left)
                left = left.left()
            while right in self.flowing:
                self.settled.add(right)
                right = right.right()

        return (direction == LEFT and left_filled) or (direction == RIGHT and right_filled)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.grid)


def main():
    start = Point(500, 0)
    grid = get_grid()
    grid[start] = '.'

    reservoir = GroundReservoir(grid)
    reservoir.fill(start)
    # Part 1: 38409
    print('Filled reservoir = {}'.format(
        len([point for point in reservoir.flowing if grid.in_range(point)])
    ))
    # Part 2: 32288
    print('Settled water = {}'.format(
        len([point for point in reservoir.settled if grid.in_range(point)])
    ))


def get_grid():
    grid = Grid()
    for line in Parser(FILE_NAME).lines():
        point_range = PointRange(line)
        for point in point_range.get_points():
            grid[point] = CLAY
    return grid


if __name__ == '__main__':
    main()

