from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


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

STATE_DIRECTION_CHANGE = {
    CLEAN: 1,
    WEAKENED: 0,
    FLAGGED: 2,
    INFECTED: -1
}


class Virus:

    def __init__(self, grid, state_chage):
        self.grid = grid
        self.state_chage = state_chage
        self.position = self.get_start_position()
        self.direction_index = 0
        self.infections = 0

    def burst(self):
        state = self.grid[self.position]
        state = CLEAN if state is None else state

        new_state = self.state_chage[state]
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
    simplified_state_change = {
        CLEAN: INFECTED,
        INFECTED: CLEAN
    }
    # Part 1: 5575
    print('Part 1: {}'.format(
        run(10_000, simplified_state_change)
    ))
    
    expanded_state_change = {
        CLEAN: WEAKENED,
        WEAKENED: INFECTED,
        FLAGGED: CLEAN,
        INFECTED: FLAGGED
    }
    # Part 2: 2511991
    print('Part 2: {}'.format(
        run(10_000_000, expanded_state_change)
    ))


def run(n, state_change):
    virus = Virus(get_grid(), state_change)
    for i in range(n):
        virus.burst()
    return virus.infections


def get_grid():
    grid = Grid()
    for y, row in enumerate(Parser().nested_lines()):
        for x, value in enumerate(row):
            point = Point(x, y)
            grid[point] = value
    return grid


if __name__ == '__main__':
    main()
