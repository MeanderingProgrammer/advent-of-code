from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


OPEN = '.'
TREES = '|'
YARD = '#'


class Landscape:

    def __init__(self, grid):
        self.grid = grid

    def step(self):
        new_grid = {}
        for point in self.grid.grid:
            value = self.grid[point]
            if value == OPEN:
                if self.count(point, TREES) >= 3:
                    new_grid[point] = TREES
            elif value == TREES:
                if self.count(point, YARD) >= 3:
                    new_grid[point] = YARD
            elif value == YARD:
                if self.count(point, YARD) == 0 or self.count(point, TREES) == 0:
                    new_grid[point] = OPEN
            else:
                raise Exception('Unknown value {}'.format(value))

        for point in new_grid:
            self.grid[point] = new_grid[point]


    def count(self, point, value):
        return sum([self.grid[adjacent] == value for adjacent in point.all_adjacent()])

    def resource_value(self):
        return self.resource_count(TREES) * self.resource_count(YARD)

    def resource_count(self, goal):
        return sum([resource == goal for point, resource in self.grid.items()])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.grid)


def main():
    # Part 1: 515496
    print('Part 1: {}'.format(run_for(10)))

    goal = 1_000_000_000
    start, pattern = get_pattern(1_000, 5, 30)
    index = (goal - start) % len(pattern)
    # Part 2: 233058
    print('Part 2: {}'.format(pattern[index]))


def run_for(n):
    landscape = Landscape(get_grid())
    for i in range(n):
        landscape.step()
    return landscape.resource_value()


def get_pattern(n, min_len, max_len):
    scores = []
    landscape = Landscape(get_grid())

    for i in range(n):
        current = landscape.resource_value()
        scores.append(current)
        landscape.step()

    return find_pattern(scores, min_len, max_len)


def find_pattern(values, min_len, max_len):
    best_pattern = None
    for i in range(len(values) - min_len):
        for j in range(i + min_len, min(i + max_len, len(values))):
            pattern = values[i:j]
            end = get_end_index(values, i, pattern)
            length = end - i
            if best_pattern is None or length > best_pattern[0]:
                best_pattern = length, i, pattern
    return best_pattern[1], best_pattern[2]


def get_end_index(values, start, pattern):
    pattern_index = 0
    for i in range(start, len(values)):
        if values[i] == pattern[pattern_index % len(pattern)]:
            pattern_index += 1
        else:
            return i
    return len(values)


def get_grid():
    grid = Grid()
    for y, row in enumerate(Parser().nested_lines()):
        for x, value in enumerate(row):
            point = Point(x, y)
            grid[point] = value
    return grid


if __name__ == '__main__':
    main()
