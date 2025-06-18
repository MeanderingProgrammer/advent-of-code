from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Box:
    length: int
    width: int
    height: int

    def paper(self) -> int:
        sides = [
            self.length * self.width,
            self.width * self.height,
            self.height * self.length,
        ]
        return sum([2 * side for side in sides]) + min(sides)

    def ribbon(self) -> int:
        sides = [self.length, self.width, self.height]
        sides.sort()
        perimeter = 2 * sides[0] + 2 * sides[1]
        volume = sides[0] * sides[1] * sides[2]
        return perimeter + volume


@answer.timer
def main() -> None:
    paper, ribbon = 0, 0
    for line in Parser().lines():
        length, width, height = line.split("x")
        box = Box(int(length), int(width), int(height))
        paper += box.paper()
        ribbon += box.ribbon()
    answer.part1(1606483, paper)
    answer.part2(3842356, ribbon)


if __name__ == "__main__":
    main()
