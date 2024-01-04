from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Box:
    l: int
    w: int
    h: int

    def paper_needed(self) -> int:
        sides = [self.l * self.w, self.w * self.h, self.h * self.l]
        return sum([2 * side for side in sides]) + min(sides)

    def ribbon_needed(self) -> int:
        sides = [self.l, self.w, self.h]
        sides.sort()
        perimeter = 2 * sides[0] + 2 * sides[1]
        volume = sides[0] * sides[1] * sides[2]
        return perimeter + volume


@answer.timer
def main() -> None:
    paper, ribbon = [], []
    for line in Parser().lines():
        box = Box(*list(map(int, line.split("x"))))
        paper.append(box.paper_needed())
        ribbon.append(box.ribbon_needed())
    answer.part1(1606483, sum(paper))
    answer.part2(3842356, sum(ribbon))


if __name__ == "__main__":
    main()
