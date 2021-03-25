from aoc_parser import Parser
from aoc_board import Grid, Point


FILE_NAME = 'data'
INPUT = '.#./..#/###'


class Art:

    def __init__(self, value):
        self.value = value.split('/')
    
    def split(self):
        components = []

        size = 2 if len(self.value) % 2 == 0 else 3
        for r in range(0, len(self.value), size):
            component_row = []
            for c in range(0, len(self.value[r]), size):
                component = []
                for i in range(size):
                    component.append(self.value[r + i][c:c+size])
                component_row.append(component)
            components.append(component_row)

        return components

    def on(self):
        count = 0
        for value in self.value:
            count += sum([v == '#' for v in value])
        return count

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join(self.value)


class Pattern:

    def __init__(self, value):
        value = value.split(' => ')
        self.matchers = self.permute(value[0])
        self.output = value[1]

    def matches(self, component):
        return '/'.join(component) in self.matchers

    def permute(self, value): 
        grid = Grid()
        for y, row in enumerate(value.split('/')):
            for x, value in enumerate(row):
                point = Point(x, y)
                grid[point] = value

        permutations = set()
        reflected = grid.reflect()

        permutations.add(self.stringify(grid))
        permutations.add(self.stringify(reflected))

        for i in range(3):
            grid = grid.rotate()
            reflected = reflected.rotate()
            permutations.add(self.stringify(grid))
            permutations.add(self.stringify(reflected))

        return permutations

    @staticmethod
    def stringify(grid):
        as_string = str(grid)
        return '/'.join(as_string.split('\n'))


def main():
    patterns = get_patterns()
    # Part 1: 188
    print('Part 1: {}'.format(run_iterations(patterns, 5)))
    # Part 2: 2758764
    print('Part 2: {}'.format(run_iterations(patterns, 18)))


def run_iterations(patterns, n):
    art = Art(INPUT)

    for i in range(n):
        rows = []
        for component_row in art.split():
            new_row = []
            for component in component_row:
                pattern = get_matching_pattern(component, patterns)
                new_row.append(pattern.output.split('/'))
            rows.extend(join_row(new_row))
        art = Art('/'.join(rows))

    return art.on()


def join_row(row):
    result = []
    for i in range(len(row[0])):
        rs = []
        for r in row:
            rs.append(r[i])
        result.append(''.join(rs))
    return result


def get_matching_pattern(component, patterns):
    for pattern in patterns:
        if pattern.matches(component):
            return pattern


def get_patterns():
    return [Pattern(line) for line in Parser(FILE_NAME).lines()]


if __name__ == '__main__':
    main()
