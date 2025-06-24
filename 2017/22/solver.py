from collections import deque

from aoc import answer
from aoc.grid import Grid, GridHelper
from aoc.parser import Parser
from aoc.point import Point, PointHelper

CLEAN = "."
WEAKENED = "W"
FLAGGED = "F"
INFECTED = "#"

DIRECTION_CHANGE = {WEAKENED: 0, CLEAN: 1, FLAGGED: 2, INFECTED: -1}


class Virus:
    def __init__(self, grid: Grid[str], change: dict[str, str]) -> None:
        self.grid: Grid[str] = grid
        self.change: dict[str, str] = change
        self.position: Point = (
            Virus.mid(GridHelper.xs(grid)),
            Virus.mid(GridHelper.ys(grid)),
        )

        self.directions: deque[Point] = deque([(0, 1), (-1, 0), (0, -1), (1, 0)])
        self.infections: int = 0

    def burst(self) -> None:
        state = self.grid.get(self.position, CLEAN)

        new_state = self.change[state]
        self.grid[self.position] = new_state
        if new_state == INFECTED:
            self.infections += 1

        self.directions.rotate(-DIRECTION_CHANGE[state])
        self.position = PointHelper.add(self.position, self.directions[0])

    @staticmethod
    def mid(values: set[int]):
        vals = sorted(values)
        return vals[len(vals) // 2]


@answer.timer
def main() -> None:
    grid = Parser().grid()

    simple = {
        CLEAN: INFECTED,
        INFECTED: CLEAN,
    }
    answer.part1(5575, run(Virus(grid.copy(), simple), 10_000))

    expanded = {
        CLEAN: WEAKENED,
        WEAKENED: INFECTED,
        FLAGGED: CLEAN,
        INFECTED: FLAGGED,
    }
    answer.part2(2511991, run(Virus(grid.copy(), expanded), 10_000_000))


def run(virus: Virus, n: int) -> int:
    for _ in range(n):
        virus.burst()
    return virus.infections


if __name__ == "__main__":
    main()
