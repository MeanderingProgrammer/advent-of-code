from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


class Operation:

    def __init__(self, value, size):
        self.value = value.split()
        self.w, self.h = size

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
                display[Point(c, (y - amount) % self.h)] for y in range(self.h)
            ]
            for y in range(self.h):
                display[Point(c, y)] = new_column[y]
        elif self.value[0] == 'rotate' and self.value[1] == 'row':
            r = int(self.value[2].split('=')[1])
            amount = int(self.value[4])
            new_row = [
                display[Point((x - amount) % self.w, r)] for x in range(self.w)
            ]
            for x in range(self.w):
                display[Point(x, r)] = new_row[x]
        else:
            raise Exception('Unknwon operation: {}'.format(self.value))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.value)


def main():
    size = 50, 6
    display = create_display(size)

    operations = get_operations(size)
    for operation in operations:
        operation.apply(display)
        
    # Part 1: 106
    print('Part 1: {}'.format(lit(display)))
    # Part 2: CFLELOYFCS
    print(display)


def lit(display):
    return sum([value == '#' for value in display.grid.values()])


def create_display(size):
    display = Grid()
    for x in range(size[0]):
        for y in range(size[1]):
            point = Point(x, y)
            display[point] = '.'
    return display


def get_operations(size):
    return [Operation(line, size) for line in Parser().lines()]


if __name__ == '__main__':
    main()
