from dataclasses import dataclass

from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point, PointHelper

DIRECTIONS: list[Point] = [(0, -1), (0, 1), (-1, 0), (1, 0)]


@dataclass
class Traverser:
    grid: Grid[str]
    pos: Point
    direction: Point
    seen: list[Point]

    def traverse(self) -> None:
        done = False
        self.seen.append(self.pos)
        while not done:
            options = self.get_options()
            if len(options) == 0:
                done = True
            elif len(options) == 1:
                self.pos, self.direction = options[0]
                self.seen.append(self.pos)
            else:
                raise Exception(f"No Idea: {self.pos} -> {options}")

    def get_options(self) -> list[tuple[Point, Point]]:
        forward = PointHelper.add(self.pos, self.direction)
        if forward in self.grid:
            return [(forward, self.direction)]
        else:
            options: list[tuple[Point, Point]] = []
            for direction in DIRECTIONS:
                new_pos = PointHelper.add(self.pos, direction)
                if self.valid(new_pos):
                    options.append((new_pos, direction))
            return options

    def valid(self, position: Point) -> bool:
        return position in self.grid and position not in self.seen

    def letters(self) -> str:
        letters: str = ""
        for position in self.seen:
            value = self.grid[position]
            if value not in ["-", "|", "+"]:
                letters += value
        return letters

    def steps(self) -> int:
        return len(self.seen)


@answer.timer
def main() -> None:
    data = Parser().nested_lines()
    grid, start = get_grid(data)
    traverser = Traverser(grid, start, DIRECTIONS[1], [])
    traverser.traverse()
    answer.part1("NDWHOYRUEA", traverser.letters())
    answer.part2(17540, traverser.steps())


def get_grid(data: list[list[str]]) -> tuple[Grid[str], Point]:
    grid: Grid[str] = dict()
    start = None
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            if value != " ":
                point = (x, y)
                grid[point] = value
                start = point if y == 0 else start
    assert start is not None
    return grid, start


if __name__ == "__main__":
    main()
