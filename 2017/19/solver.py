from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point, PointHelper

DIRECTIONS: list[Point] = [(0, -1), (0, 1), (-1, 0), (1, 0)]


class Traverser:
    def __init__(self, grid: Grid[str]):
        self.grid = grid
        self.pos = self.get_start()
        self.direction = DIRECTIONS[1]
        self.seen = [self.pos]

    def get_start(self) -> Point:
        for point in self.grid:
            if point[1] == 0:
                return point
        raise Exception("Failed")

    def traverse(self) -> None:
        done = False
        while not done:
            options = self.get_options()
            if len(options) == 0:
                done = True
            elif len(options) == 1:
                self.direction, self.pos = options[0]
                self.seen.append(self.pos)
            else:
                raise Exception(f"No Idea: {self.pos} -> {options}")

    def get_options(self) -> list[tuple[Point, Point]]:
        forward = PointHelper.add(self.pos, self.direction)
        if forward in self.grid:
            return [(self.direction, forward)]
        else:
            options = []
            for direction in DIRECTIONS:
                new_pos = PointHelper.add(self.pos, direction)
                if self.valid_position(new_pos):
                    options.append((direction, new_pos))
            return options

    def valid_position(self, position: Point) -> bool:
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
    traverser = Traverser(get_grid())
    traverser.traverse()
    answer.part1("NDWHOYRUEA", traverser.letters())
    answer.part2(17540, traverser.steps())


def get_grid() -> Grid[str]:
    grid: Grid = dict()
    for y, line in enumerate(Parser().nested_lines()):
        for x, value in enumerate(line):
            if value != " ":
                grid[(x, y)] = value
    return grid


if __name__ == "__main__":
    main()
