from dataclasses import dataclass
from typing import List, Tuple

from aoc import answer
from aoc.board import Grid, Point
from aoc.int_code import Computer
from aoc.parser import Parser

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


@dataclass
class Direction:
    index: int = 0

    def rotate(self, value: int) -> None:
        self.index += value if value == 1 else -1

    def step(self, position: Tuple[int, int]) -> Tuple[int, int]:
        to_go = DIRECTIONS[self.index % len(DIRECTIONS)]
        return position[0] + to_go[0], position[1] + to_go[1]


class PaintBot:
    def __init__(self, memory: List[int], starting_color: int):
        self.computer = Computer(self)
        self.computer.set_memory(memory)

        self.color = True

        self.direction = Direction()
        self.grid = {}
        self.position = (0, 0)
        self.grid[self.position] = starting_color

    def run(self) -> None:
        self.computer.run()

    def get_input(self) -> int:
        return self.grid[self.position] if self.position in self.grid else 0

    def add_output(self, value: int) -> None:
        if self.color:
            self.grid[self.position] = value
        else:
            self.direction.rotate(value)
            self.position = self.direction.step(self.position)
        self.color = not self.color

    def get_grid(self) -> Grid:
        grid = Grid()
        for position, value in self.grid.items():
            point = Point(*position)
            grid[point] = "." if value == 0 else "#"
        return grid


def main():
    answer.part1(1909, len(run(0).grid))
    expected = [
        "...##.#..#.####.####.#..#.#..#.###..#..#...",
        "....#.#..#.#....#....#.#..#..#.#..#.#..#...",
        "....#.#..#.###..###..##...####.#..#.####...",
        "....#.#..#.#....#....#.#..#..#.###..#..#...",
        ".#..#.#..#.#....#....#.#..#..#.#....#..#...",
        "..##...##..#....####.#..#.#..#.#....#..#...",
    ]
    answer.part2("\n" + "\n".join(expected), "\n" + str(run(1).get_grid()))


def run(setting: int) -> PaintBot:
    bot = PaintBot(Parser().int_csv(), setting)
    bot.run()
    return bot


if __name__ == "__main__":
    main()
