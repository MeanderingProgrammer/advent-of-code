from collections import deque

import commons.answer as answer
from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


CLEAN = '.'
WEAKENED = 'W'
FLAGGED = 'F'
INFECTED = '#'

STATE_DIRECTION_CHANGE = {
    WEAKENED: 0,
    CLEAN: 1,
    FLAGGED: 2,
    INFECTED: -1
}


class Virus:

    def __init__(self, grid, state_chage):
        self.grid = grid
        self.state_chage = state_chage
        self.position = self.get_start_position()

        self.directions = deque([
            Point(0, 1), 
            Point(-1, 0), 
            Point(0, -1), 
            Point(1, 0)
        ])
        self.infections = 0

    def burst(self):
        state = self.grid.get(self.position, CLEAN)

        new_state = self.state_chage[state]
        self.grid[self.position] = new_state

        if new_state == INFECTED:
            self.infections += 1

        self.directions.rotate(-STATE_DIRECTION_CHANGE[state])
        self.position += self.directions[0]

    def get_start_position(self):
        x = self.mid(self.grid.xs())
        y = self.mid(self.grid.ys())
        return Point(x, y)

    @staticmethod
    def mid(values):
        values = list(values)
        values.sort()
        return values[len(values) // 2]


def main():
    simplified_state_change = {
        CLEAN: INFECTED,
        INFECTED: CLEAN
    }
    answer.part1(5575, run(10_000, simplified_state_change))
    
    expanded_state_change = {
        CLEAN: WEAKENED,
        WEAKENED: INFECTED,
        FLAGGED: CLEAN,
        INFECTED: FLAGGED
    }
    answer.part2(2511991, run(10_000_000, expanded_state_change))


def run(n, state_change):
    virus = Virus(get_grid(), state_change)
    for i in range(n):
        virus.burst()
    return virus.infections


def get_grid():
    return Parser().as_grid()


if __name__ == '__main__':
    main()
