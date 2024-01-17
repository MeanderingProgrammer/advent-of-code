from dataclasses import dataclass
from typing import override

from aoc import answer
from aoc.grid import Grid, GridHelper
from aoc.int_code import Bus, Computer
from aoc.parser import Parser
from aoc.point import Point, PointHelper

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


@dataclass
class Direction:
    index: int = 0

    def rotate(self, value: int) -> None:
        self.index += value if value == 1 else -1

    def step(self, position: Point) -> tuple[int, int]:
        to_go = DIRECTIONS[self.index % len(DIRECTIONS)]
        return PointHelper.add(position, to_go)


@dataclass
class PaintBot(Bus):
    direction: Direction
    position: Point
    grid: Grid[int]
    color: bool = True

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        return self.grid[self.position] if self.position in self.grid else 0

    @override
    def add_output(self, value: int) -> None:
        if self.color:
            self.grid[self.position] = value
        else:
            self.direction.rotate(value)
            self.position = self.direction.step(self.position)
        self.color = not self.color

    def grid_str(self) -> str:
        grid = dict()
        for point, value in self.grid.items():
            grid[point] = "." if value == 0 else "#"
        return GridHelper.to_str(grid)


@answer.timer
def main() -> None:
    answer.part1(1909, len(run(0).grid))
    expected = [
        "...##.#..#.####.####.#..#.#..#.###..#..#...",
        "....#.#..#.#....#....#.#..#..#.#..#.#..#...",
        "....#.#..#.###..###..##...####.#..#.####...",
        "....#.#..#.#....#....#.#..#..#.###..#..#...",
        ".#..#.#..#.#....#....#.#..#..#.#....#..#...",
        "..##...##..#....####.#..#.#..#.#....#..#...",
    ]
    answer.part2("\n" + "\n".join(expected), "\n" + run(1).grid_str())


def run(setting: int) -> PaintBot:
    bot = PaintBot(
        direction=Direction(),
        position=(0, 0),
        grid={(0, 0): setting},
    )
    Computer(bus=bot, memory=Parser().int_csv()).run()
    return bot


if __name__ == "__main__":
    main()
