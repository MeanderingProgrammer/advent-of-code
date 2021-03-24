from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'

CLEAN = '.'
WEAKENED = 'W'
FLAGGED = 'F'
INFECTED = '#'



U = Point(0, -1)
D = Point(0, 1)
L = Point(-1, 0)
R = Point(1, 0)

DIRECTIONS = [
    U, L, D, R
]

STATE_CHANGE = {
    CLEAN: WEAKENED,
    WEAKENED: INFECTED,
    FLAGGED: CLEAN,
    INFECTED: FLAGGED
}


STATE_DIRECTION_CHANGE = {
    CLEAN: 1,
    WEAKENED: 0,
    FLAGGED: 2,
    INFECTED: -1
}

class Virus:

    def __init__(self, grid):
        self.grid = grid
        self.position = self.get_start_position()
        self.direction_index = 0
        self.infections = 0

    def burst(self):
        state = self.grid[self.position]
        state = CLEAN if state is None else state

        new_state = STATE_CHANGE[state]
        self.grid[self.position] = new_state

        if new_state == INFECTED:
            self.infections += 1

        update_direction = STATE_DIRECTION_CHANGE[state]
        self.direction_index += update_direction
        self.direction_index %= len(DIRECTIONS)

        self.position += DIRECTIONS[self.direction_index]

    def get_start_position(self):
        xs = list(self.grid.xs())
        xs.sort()
        x = xs[len(xs)//2]

        ys = list(self.grid.ys())
        ys.sort()
        y = ys[len(ys)//2]

        return Point(x, y)


def main():
    virus = Virus(get_grid())

    for i in range(10_000_000):
        if i % 100_000 == 0:
            print(i)
        virus.burst()

    # Part 1 = 5575
    # Part 2 = 2511991
    print('Infections = {}'.format(virus.infections))


def get_grid():
    grid = Grid()
    for y, row in enumerate(Parser(FILE_NAME).nested_lines()):
        for x, value in enumerate(row):
            point = Point(x, y)
            grid[point] = value
    return grid



if __name__ == '__main__':
    main()

