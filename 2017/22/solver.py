from collections import deque

from aoc import answer
from aoc.grid import Grid, GridHelper
from aoc.parser import Parser
from aoc.point import PointHelper

CLEAN = "."
WEAKENED = "W"
FLAGGED = "F"
INFECTED = "#"

STATE_DIRECTION_CHANGE = {WEAKENED: 0, CLEAN: 1, FLAGGED: 2, INFECTED: -1}


class Virus:
    def __init__(self, grid: Grid, state_chage: dict[str, str]):
        self.grid = grid
        self.state_chage = state_chage
        self.position = (Virus.mid(GridHelper.xs(grid)), Virus.mid(GridHelper.ys(grid)))

        self.directions = deque([(0, 1), (-1, 0), (0, -1), (1, 0)])
        self.infections = 0

    def burst(self) -> None:
        state: str = self.grid.get(self.position, CLEAN)

        new_state = self.state_chage[state]
        self.grid[self.position] = new_state
        if new_state == INFECTED:
            self.infections += 1

        self.directions.rotate(-STATE_DIRECTION_CHANGE[state])
        self.position = PointHelper.add(self.position, self.directions[0])

    @staticmethod
    def mid(values: set[int]):
        as_list = list(values)
        as_list.sort()
        return as_list[len(values) // 2]


@answer.timer
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
    virus = Virus(Parser().grid(), state_change)
    for _ in range(n):
        virus.burst()
    return virus.infections


if __name__ == "__main__":
    main()
