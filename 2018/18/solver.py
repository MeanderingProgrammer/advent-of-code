from dataclasses import dataclass

from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point, PointHelper

OPEN, TREES, YARD = ".", "|", "#"


@dataclass(frozen=True)
class Landscape:
    grid: Grid[str]

    def step(self) -> None:
        new_grid: Grid[str] = dict()
        for point, value in self.grid.items():
            if value == OPEN:
                if self.count(point, TREES) >= 3:
                    new_grid[point] = TREES
            elif value == TREES:
                if self.count(point, YARD) >= 3:
                    new_grid[point] = YARD
            elif value == YARD:
                if self.count(point, YARD) == 0 or self.count(point, TREES) == 0:
                    new_grid[point] = OPEN
            else:
                raise Exception(f"Unknown value {value}")
        for point in new_grid:
            self.grid[point] = new_grid[point]

    def count(self, point: Point, value: str) -> int:
        neighbors = PointHelper.neighbors_diagonal(point)
        return sum([self.grid.get(neighbor) == value for neighbor in neighbors])

    def resource_value(self) -> int:
        return self.resource_count(TREES) * self.resource_count(YARD)

    def resource_count(self, goal: str) -> int:
        return sum([resource == goal for _, resource in self.grid.items()])


@answer.timer
def main() -> None:
    answer.part1(515496, run_for(10))
    answer.part2(233058, run_for(1_000_000_000))


def run_for(n: int) -> int:
    landscape = Landscape(get_grid())
    scores = [landscape.resource_value()]
    for _ in range(n):
        landscape.step()
        scores.append(landscape.resource_value())
        start, pattern = find_pattern(scores)
        if start is not None:
            index = (n - start) % len(pattern)
            return pattern[index]
    return scores[-1]


def find_pattern(values: list[int]) -> tuple[int | None, list[int]]:
    for i in range(1, len(values) - 1):
        if values[i] == values[-1] and values[i - 1] == values[-2]:
            return i - 1, values[i - 1 : -2]
    return None, []


def get_grid() -> Grid[str]:
    grid: Grid[str] = dict()
    for y, row in enumerate(Parser().nested_lines()):
        for x, value in enumerate(row):
            grid[(x, y)] = value
    return grid


if __name__ == "__main__":
    main()
