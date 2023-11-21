from collections import deque

from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser

CLEAN = "."
WEAKENED = "W"
FLAGGED = "F"
INFECTED = "#"

STATE_DIRECTION_CHANGE = {WEAKENED: 0, CLEAN: 1, FLAGGED: 2, INFECTED: -1}


class Virus:
    def __init__(self, grid: Grid, state_chage: dict[str, str]):
        self.grid = grid
        self.state_chage = state_chage
        self.position = Point(Virus.mid(grid.xs()), Virus.mid(grid.ys()))

        self.directions = deque([Point(0, 1), Point(-1, 0), Point(0, -1), Point(1, 0)])
        self.infections = 0

    def burst(self) -> None:
        state: str = self.grid.get(self.position, CLEAN)

        new_state = self.state_chage[state]
        self.grid[self.position] = new_state
        if new_state == INFECTED:
            self.infections += 1

        self.directions.rotate(-STATE_DIRECTION_CHANGE[state])
        self.position += self.directions[0]

    @staticmethod
    def mid(values):
        values = list(values)
        values.sort()
        return values[len(values) // 2]


def main() -> None:
    simplified_state_change = {CLEAN: INFECTED, INFECTED: CLEAN}
    answer.part1(5575, run(10_000, simplified_state_change))

    expanded_state_change = {
        CLEAN: WEAKENED,
        WEAKENED: INFECTED,
        FLAGGED: CLEAN,
        INFECTED: FLAGGED,
    }
    answer.part2(2511991, run(10_000_000, expanded_state_change))


def run(n: int, state_change: dict[str, str]) -> int:
    virus = Virus(Parser().as_grid(), state_change)
    for _ in range(n):
        virus.burst()
    return virus.infections


if __name__ == "__main__":
    main()
