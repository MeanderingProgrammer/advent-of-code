import sys
from dataclasses import dataclass

from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point

sys.setrecursionlimit(10_000)

CLAY = "#"
DOWN = "d"
LEFT = "l"
RIGHT = "r"


@dataclass(frozen=True)
class GroundReservoir:
    grid: Grid[str]
    min_y: int
    max_y: int
    flowing: set[Point]
    settled: set[Point]

    def fill(self, point: Point, direction: str) -> bool:
        if self.grid.get(point) == CLAY:
            return True

        self.flowing.add(point)

        down = (point[0], point[1] + 1)
        if not self.grid.get(down) == CLAY:
            if down not in self.flowing and self.in_range(down, False):
                self.fill(down, DOWN)
            if down not in self.settled:
                return False

        left = (point[0] - 1, point[1])
        left_filled = left not in self.flowing and self.fill(left, LEFT)

        right = (point[0] + 1, point[1])
        right_filled = right not in self.flowing and self.fill(right, RIGHT)

        # All water at this 'level' has settled
        if direction == DOWN and left_filled and right_filled:
            self.settled.add(point)
            while left in self.flowing:
                self.settled.add(left)
                left = (left[0] - 1, left[1])
            while right in self.flowing:
                self.settled.add(right)
                right = (right[0] + 1, right[1])

        left_condition = direction == LEFT and left_filled
        right_condition = direction == RIGHT and right_filled
        return left_condition or right_condition

    def in_range(self, point: Point, use_min: bool = True) -> bool:
        min_value = self.min_y if use_min else 1
        return point[1] >= min_value and point[1] <= self.max_y


@answer.timer
def main() -> None:
    grid = get_grid()
    grid[(500, 0)] = "."
    ys = set([point[1] for point in grid])
    ys.remove(0)
    reservoir = GroundReservoir(
        grid=grid,
        min_y=min(ys),
        max_y=max(ys),
        flowing=set(),
        settled=set(),
    )
    reservoir.fill((500, 0), DOWN)
    answer.part1(38409, sum([reservoir.in_range(point) for point in reservoir.flowing]))
    answer.part2(32288, sum([reservoir.in_range(point) for point in reservoir.settled]))


def get_grid() -> Grid[str]:
    def parse_range(value: str) -> list[int]:
        parts = value.split("..")
        if len(parts) == 1:
            return [int(parts[0])]
        else:
            return list(range(int(parts[0]), int(parts[1]) + 1))

    def parse_point_range(line: str) -> list[Point]:
        coord_range: dict[str, list[int]] = dict()
        for part in line.split(", "):
            coord, value = part.split("=")
            coord_range[coord] = parse_range(value)
        points: list[Point] = []
        for x in coord_range["x"]:
            for y in coord_range["y"]:
                points.append((x, y))
        return points

    grid: Grid[str] = dict()
    for line in Parser().lines():
        for point in parse_point_range(line):
            grid[point] = CLAY
    return grid


if __name__ == "__main__":
    main()
