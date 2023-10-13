from aoc import answer
from aoc.parser import Parser
from itertools import product
from collections import defaultdict

SINGLE = {
    "turn on": lambda current: 1,
    "turn off": lambda current: 0,
    "toggle": lambda current: 1 - current,
}

DIMABLE = {
    "turn on": lambda current: current + 1,
    "turn off": lambda current: max(current - 1, 0),
    "toggle": lambda current: current + 2,
}


class PointRange:
    def __init__(self, value):
        self.bottom_left = self.to_point(value[0])
        self.top_right = self.to_point(value[2])

    def get_points(self):
        return product(
            range(self.bottom_left[0], self.top_right[0] + 1),
            range(self.bottom_left[1], self.top_right[1] + 1),
        )

    @staticmethod
    def to_point(coords):
        return [int(coord) for coord in coords.split(",")]


class Direction:
    def __init__(self, value):
        value = value.split()
        self.action = " ".join(value[:-3])
        self.point_range = PointRange(value[-3:])

    def apply(self, grid):
        for point in self.point_range.get_points():
            grid[point].append(self.action)


def main():
    grid_values = run_grid()
    answer.part1(400410, state_value(grid_values, SINGLE))
    answer.part2(15343601, state_value(grid_values, DIMABLE))


def run_grid():
    directions = get_directions()
    grid = defaultdict(list)
    for direction in directions:
        direction.apply(grid)
    return grid.values()


def state_value(grid_values, state_change_impacts):
    total = 0
    for grid_value in grid_values:
        current = 0
        for state_change in grid_value:
            current = state_change_impacts[state_change](current)
        total += current
    return total


def get_directions():
    return [Direction(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
