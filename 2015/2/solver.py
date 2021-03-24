from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class Box:

    def __init__(self, l, w, h):
        self.l = int(l)
        self.w = int(w)
        self.h = int(h)

    def paper_needed(self):
        sides = [
            self.l*self.w,
            self.w*self.h,
            self.h*self.l
        ]
        return sum([2*side for side in sides]) + min(sides)

    def ribbon_needed(self):
        sides = [self.l, self.w, self.h]
        sides.sort()
        perimeter = 2*sides[0] + 2*sides[1]
        volume = sides[0]*sides[1]*sides[2]
        return perimeter + volume



def main():
    paper, ribbon = [], []
    for line in Parser(FILE_NAME).lines():
        box = Box(*line.split('x'))
        paper.append(box.paper_needed())
        ribbon.append(box.ribbon_needed())
    # Part 1 = 1606483
    print('Paper needed = {}'.format(sum(paper)))
    # Part 2 = 3842356
    print('Ribbon needed = {}'.format(sum(ribbon)))


if __name__ == '__main__':
    main()

