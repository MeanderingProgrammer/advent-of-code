from dataclasses import dataclass

from aoc import answer
from aoc.grid import Grid, GridHelper
from aoc.parser import Parser
from aoc.point import Point


@dataclass(frozen=True)
class Operation:
    value: list[str]
    w: int
    h: int

    def apply(self, display: Grid) -> None:
        if self.value[0] == "rect":
            c, r = [int(v) for v in self.value[1].split("x")]
            for x in range(c):
                for y in range(r):
                    point = (x, y)
                    display[point] = "#"
        elif self.value[0] == "rotate" and self.value[1] == "column":
            c = int(self.value[2].split("=")[1])
            amount = int(self.value[4])
            new_column = [display[(c, (y - amount) % self.h)] for y in range(self.h)]
            for y in range(self.h):
                display[(c, y)] = new_column[y]
        elif self.value[0] == "rotate" and self.value[1] == "row":
            r = int(self.value[2].split("=")[1])
            amount = int(self.value[4])
            new_row = [display[((x - amount) % self.w, r)] for x in range(self.w)]
            for x in range(self.w):
                display[(x, r)] = new_row[x]
        else:
            raise Exception(f"Unknwon operation: {self.value}")


@answer.timer
def main() -> None:
    w, h = 50, 6
    display = create_display(w, h)
    operations = [Operation(line.split(), w, h) for line in Parser().lines()]
    for operation in operations:
        operation.apply(display)
    display = GridHelper.mirror(display)

    answer.part1(106, lit(display))
    expected = [
        ".##..####.#....####.#.....##..#...#####..##...###.",
        "#..#.#....#....#....#....#..#.#...##....#..#.#....",
        "#....###..#....###..#....#..#..#.#.###..#....#....",
        "#....#....#....#....#....#..#...#..#....#.....##..",
        "#..#.#....#....#....#....#..#...#..#....#..#....#.",
        ".##..#....####.####.####..##....#..#.....##..###..",
    ]
    answer.part2("\n" + "\n".join(expected), "\n" + GridHelper.to_str(display))


def create_display(w: int, h: int) -> Grid[str]:
    display: Grid[str] = dict()
    for x in range(w):
        for y in range(h):
            display[(x, y)] = "."
    return display


def lit(display: Grid[str]) -> int:
    return sum([value == "#" for _, value in display.items()])


if __name__ == "__main__":
    main()
