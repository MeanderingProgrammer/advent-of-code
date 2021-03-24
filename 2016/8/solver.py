from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'

SIZE = 50, 6


class Operation:

    def __init__(self, value):
        self.value = value.split()

    def apply(self, display):
        if self.value[0] == 'rect':
            c, r = [int(v) for v in self.value[1].split('x')]
            for x in range(c):
                for y in range(r):
                    point = Point(x, y)
                    display[point] = '#'
        elif self.value[0] == 'rotate' and self.value[1] == 'column':
            c = int(self.value[2].split('=')[1])
            amount = int(self.value[4])
            new_column = [
                display[Point(c, (y - amount) % SIZE[1])] for y in range(SIZE[1])
            ]
            for y in range(SIZE[1]):
                display[Point(c, y)] = new_column[y]
        elif self.value[0] == 'rotate' and self.value[1] == 'row':
            r = int(self.value[2].split('=')[1])
            amount = int(self.value[4])
            new_row = [
                display[Point((x - amount) % SIZE[0], r)] for x in range(SIZE[0])
            ]
            for x in range(SIZE[0]):
                display[Point(x, r)] = new_row[x]
        else:
            raise Exception('Unknwon operation: {}'.format(self.value))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.value)


def main():
    display = create_display()

    operations = get_operations()
    for operation in operations:
        operation.apply(display)
        
    # Part 1 = 106
    print('Total lit = {}'.format(lit(display)))
    # Part 2 = CFLELOYFCS
    print(display)


def lit(display):
    return sum([value == '#' for value in display.grid.values()])


def create_display():
    display = Grid()
    for x in range(SIZE[0]):
        for y in range(SIZE[1]):
            point = Point(x, y)
            display[point] = '.'
    return display


def get_operations():
    return [Operation(line) for line in Parser(FILE_NAME).lines()]


if __name__ == '__main__':
    main()

