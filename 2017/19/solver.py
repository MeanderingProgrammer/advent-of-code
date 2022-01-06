import commons.answer as answer
from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


class Traverser:

    def __init__(self, grid):
        self.grid = grid

        self.pos = self.get_start()
        self.direction = DOWN

        self.done = False
        self.seen = [self.pos]

    def get_start(self):
        for x in self.grid.xs():
            point = Point(x, 0)
            if point in self.grid:
                return point

    def traverse(self):
        while not self.done:
            options = self.get_options()
            if len(options) == 0:
                self.done = True
            elif len(options) > 1:
                raise Exception('No Idea: {} -> {}'.format(self.pos, options))
            else:
                self.direction, self.pos = options[0]
                self.seen.append(self.pos)

    def get_options(self):
        same_direction = self.pos + self.direction
        if same_direction in self.grid:
            return [(self.direction, same_direction)]
        else:
            options = []
            for direction in DIRECTIONS:
                new_pos = self.pos + direction
                if self.valid_position(new_pos):
                    options.append((direction, new_pos))
            return options

    def valid_position(self, position):
        return position in self.grid and position not in self.seen

    def letters(self):
        letters = []
        for position in self.seen:
            value = self.grid[position]
            if value not in ['-', '|', '+']:
                letters.append(value)
        return ''.join(letters)

    def steps(self):
        return len(self.seen)


def main():
    grid = get_grid()
    traverser = Traverser(grid)
    traverser.traverse()
    answer.part1('NDWHOYRUEA', traverser.letters())
    answer.part2(17540, traverser.steps())


def get_grid():
    grid = Grid()
    for y, line in enumerate(Parser().nested_lines()):
        for x, value in enumerate(line):
            point = Point(x, y)
            if value != ' ':
                grid[point] = value
    return grid


if __name__ == '__main__':
    main()
