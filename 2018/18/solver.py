from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser
from typing import List, Optional, Tuple

OPEN = "."
TREES = "|"
YARD = "#"


class Landscape:
    def __init__(self, grid):
        self.grid = grid

    def step(self):
        new_grid = {}
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
                raise Exception("Unknown value {}".format(value))

        for point in new_grid:
            self.grid[point] = new_grid[point]

    def count(self, point, value):
        return sum([self.grid[adjacent] == value for adjacent in point.adjacent(True)])

    def resource_value(self):
        return self.resource_count(TREES) * self.resource_count(YARD)

    def resource_count(self, goal):
        return sum([resource == goal for _, resource in self.grid.items()])


def main():
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


def find_pattern(values: List[int]) -> Tuple[Optional[int], List[int]]:
    for i in range(1, len(values) - 1):
        if values[i] == values[-1] and values[i - 1] == values[-2]:
            return i - 1, values[i - 1 : -2]
    return None, []


def get_grid():
    grid = Grid()
    for y, row in enumerate(Parser().nested_lines()):
        for x, value in enumerate(row):
            point = Point(x, y)
            grid[point] = value
    return grid


if __name__ == "__main__":
    main()
