from aoc import answer
from aoc.parser import Parser


class Box:
    def __init__(self, l, w, h):
        self.l = int(l)
        self.w = int(w)
        self.h = int(h)

    def paper_needed(self):
        sides = [self.l * self.w, self.w * self.h, self.h * self.l]
        return sum([2 * side for side in sides]) + min(sides)

    def ribbon_needed(self):
        sides = [self.l, self.w, self.h]
        sides.sort()
        perimeter = 2 * sides[0] + 2 * sides[1]
        volume = sides[0] * sides[1] * sides[2]
        return perimeter + volume


def main():
    paper, ribbon = [], []
    for line in Parser().lines():
        box = Box(*line.split("x"))
        paper.append(box.paper_needed())
        ribbon.append(box.ribbon_needed())
    answer.part1(1606483, sum(paper))
    answer.part2(3842356, sum(ribbon))


if __name__ == "__main__":
    main()
