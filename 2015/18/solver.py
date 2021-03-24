import math
import itertools
from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'

ON = '#'
OFF = '.'

ADJACENTS = [
    Point(0, 1),
    Point(1, 1),
    Point(1, 0),
    Point(-1, 1),
    Point(-1, 0),
    Point(-1, -1),
    Point(0, -1),
    Point(1, -1)
]


class Animator:

    def __init__(self, grid, force_corners):
        self.grid = grid
        self.force_corners = force_corners

        xs = self.grid.xs()
        ys = self.grid.ys()

        self.corners = [
            Point(min(xs), min(ys)),
            Point(min(xs), max(ys)),
            Point(max(xs), min(ys)),
            Point(max(xs), max(ys))
        ]
        self.flip_corners()

    def flip_corners(self):
        if not self.force_corners:
            return
        for corner in self.corners:
            self.grid[corner] = ON

    def step(self):
        next_grid = Grid()
        for point, value in self.grid.items():
            new_value = OFF
            neighbors_on = self.neighbors_on(point)

            if value == ON and neighbors_on in [2, 3]:
                new_value = ON
            elif value == OFF and neighbors_on == 3:
                new_value = ON

            next_grid[point] = new_value
        self.grid = next_grid
        self.flip_corners()

    def neighbors_on(self, point):
        on = 0
        for adjacent in ADJACENTS:
            adjacent += point
            if self.grid[adjacent] == ON:
                on += 1
        return on

    def lights_on(self):
        return sum([value == ON for (key, value) in self.grid.items()])


def main():
    # Part 1 = 1061
    run(False)
    # Part 2 = 1006
    run(True)


def run(force_corners):
    animator = Animator(get_grid(), force_corners)
    for i in range(100):
        print(i)
        animator.step()
    print(animator.lights_on())


def get_grid():
    grid = Grid()
    for y, line in enumerate(Parser(FILE_NAME).lines()):
        for x, value in enumerate(line):
            point = Point(x, y)
            grid[point] = value
    return grid


if __name__ == '__main__':
    main()

