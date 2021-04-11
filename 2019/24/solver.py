from commons.aoc_parser import Parser


INNER_GRID = '?'
ALIVE = '#'
EMPTY = '.'


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self, grid):
        return grid[self.y][self.x]

    def left(self):
        return Point(self.x-1, self.y)

    def right(self):
        return Point(self.x+1, self.y)

    def up(self):
        return Point(self.x, self.y-1)

    def down(self):
        return Point(self.x, self.y+1)

    def is_outside(self):
        if self.x < 0 or self.y < 0:
            return True
        elif self.x > 4 or self.y > 4:
            return True
        else:
            return False

    def is_inside(self):
        return self.x == 2 and self.y == 2

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)


class Element:

    def __init__(self, value='.'):
        self.value = value
        self.next_state = None

    def alive(self):
        return 1 if self.value == ALIVE else 0

    def set_next_state(self, count):
        if self.value == ALIVE:
            self.next_state = ALIVE if count == 1 else EMPTY
        else:
            self.next_state = ALIVE if count in [1, 2] else EMPTY

    def update_state(self):
        self.value = self.next_state
        self.next_state = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return INNER_GRID if self.value is None else self.value


class Grid:

    def __init__(self, values=None):
        if values is None:
            self.grid = [[Element() for c in range(5)] for r in range(5)]
        else:
            self.grid = [[Element(element) for element in value] for value in values]

    def step(self, previous_level=None, next_level=None):
        previous_counts = [
            0 if previous_level is None else previous_level.inner_top(),
            0 if previous_level is None else previous_level.inner_bottom(),
            0 if previous_level is None else previous_level.inner_left(),
            0 if previous_level is None else previous_level.inner_right()
        ]
        next_counts = [
            0 if next_level is None else next_level.outer_bottom(),
            0 if next_level is None else next_level.outer_top(),
            0 if next_level is None else next_level.outer_right(),
            0 if next_level is None else next_level.outer_left()
        ]
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                point = Point(c, r)
                if not point.is_inside():
                    count = self.count_adjacent(point, previous_counts, next_counts)
                    value.set_next_state(count)

    def update(self):
        for row in self.grid:
            for value in row:
                value.update_state()

    def inner_left(self):
        return self.grid[2][1].alive()

    def inner_right(self):
        return self.grid[2][3].alive()

    def inner_top(self):
        return self.grid[1][2].alive()

    def inner_bottom(self):
        return self.grid[3][2].alive()

    def outer_left(self):
        return sum([row[0].alive() for row in self.grid])

    def outer_right(self):
        return sum([row[4].alive() for row in self.grid])

    def outer_top(self):
        return sum([value.alive() for value in self.grid[0]])

    def outer_bottom(self):
        return sum([value.alive() for value in self.grid[4]])

    def count_adjacent(self, point, previous_counts, next_counts):
        adjacent_points = [
            (point.up(), previous_counts[0], next_counts[0]),
            (point.down(), previous_counts[1], next_counts[1]),
            (point.left(), previous_counts[2], next_counts[2]),
            (point.right(), previous_counts[3], next_counts[3])
        ]

        counts = []
        for adjacent_point, outside, inside in adjacent_points:
            if adjacent_point.is_outside():
                counts.append(outside)
            elif adjacent_point.is_inside():
                counts.append(inside)
            else:
                counts.append(adjacent_point.get(self.grid).alive())
        return sum(counts)

    def count(self):
        return sum(self.flatten())

    def diversity(self):
        total = 0
        for i, value in enumerate(self.flatten()):
            total += pow(2, i) * value
        return total

    def flatten(self):
        return [value.alive() for row in self.grid for value in row]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join([''.join([str(element) for element in row]) for row in self.grid])


class RecursiveGrid:

    def __init__(self, values):
        self.levels = [
            Grid(values)
        ]

    def step(self):
        self.levels = [Grid()] + self.levels + [Grid()]
        total_levels = len(self.levels)
        for index, level in enumerate(self.levels):
            previous_level = self.levels[index-1] if index > 0 else None
            next_level = self.levels[index+1] if index < total_levels - 1 else None
            level.step(previous_level, next_level)
        # Update all levels at end to avoid using updated state in next state calculations
        [level.update() for level in self.levels]

    def count_bugs(self):
        return sum([level.count() for level in self.levels])

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = []
        current_level = ((len(self.levels) - 1) // 2) * -1
        for level in self.levels:
            result.append('Depth {}:'.format(current_level))
            result.append('{}'.format(level))
            current_level += 1
        return '\n'.join(result)


def main():
    # Part 1: 32776479
    print('Part 1: {}'.format(solve_part_1()))
    # Part 2: 2017
    print('Part 2: {}'.format(solve_part_2()))


def solve_part_1():
    seen = set()
    grid = Grid(get_data())
    while str(grid) not in seen:
        seen.add(str(grid))
        grid.step()
        grid.update()
    return grid.diversity()


def solve_part_2():
    grid = RecursiveGrid(get_data())
    for i in range(200):
        grid.step()
    return grid.count_bugs()


def get_data():
    return Parser().nested_lines()


if __name__ == '__main__':
    main()
