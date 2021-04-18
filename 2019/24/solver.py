from commons.aoc_parser import Parser
from commons.aoc_board import Point, Grid


ALIVE = '#'
EMPTY = '.'

MIDDLE = Point(2, 2)


class Layout:

    def __init__(self, grid, recursive):
        self.grids = [grid]
        self.recursive = recursive

    def step(self):
        if self.recursive:
            self.grids = [self.new_grid()] + self.grids + [self.new_grid()]

        next_grids = []

        for level, grid in enumerate(self.grids):
            next_grid = Grid()

            for point, value in grid.items():
                if not self.recursive or point != MIDDLE:
                    bugs_adjacent = self.get_bugs_adjacent(level, point)
                    if value == ALIVE:
                        next_value = ALIVE if bugs_adjacent == 1 else EMPTY
                    else:
                        next_value = ALIVE if bugs_adjacent in [1, 2] else EMPTY
                    next_grid[point] = next_value

            next_grids.append(next_grid)

        self.grids = next_grids

    def new_grid(self):
        grid = Grid()
        for point, value in self.grids[0].items():
            grid[point] = EMPTY
        return grid

    def get_bugs_adjacent(self, level, point):
        bugs = 0
        current_grid = self.grids[level]
        for adjacent in point.adjacent():
            if self.recursive and adjacent == MIDDLE:
                # Count the correct inside edge down one level
                inner_level = level - 1
                if inner_level >= 0:
                    inner_grid = self.grids[inner_level]
                    bugs += self.count_inner(point, inner_grid)
            elif self.recursive and adjacent not in current_grid:
                # Get the correct value up one level
                outer_level = level + 1
                if outer_level < len(self.grids):
                    outer_grid = self.grids[outer_level]
                    bugs += self.count_outer(point, adjacent, outer_grid)
            else:
                # A standard point that we can check at the current level
                if current_grid[adjacent] == ALIVE:
                    bugs += 1
        return bugs

    def count_inner(self, original, grid):
        if original.up() == MIDDLE:
            # If going up from original led to the inner grid then we are
            # interested in the bottom row of points
            point_of_interest = lambda point: point.y() == 0
        elif original.down() == MIDDLE:
            # If going down original led to the inner grid then we are
            # interested in the top row of points
            point_of_interest = lambda point: point.y() == 4
        elif original.left() == MIDDLE:
            # If going left from original led to the inner grid then we are
            # interested in the right most points
            point_of_interest = lambda point: point.x() == 4
        elif original.right() == MIDDLE:
            # If going right from original led to the inner grid then we are
            # interested in the left most points
            point_of_interest = lambda point: point.x() == 0
        else:
            raise Exception('Unhandled original point')
        return sum([value == ALIVE for point, value in grid.items() if point_of_interest(point)])

    def count_outer(self, original, adjacent, grid):
        if original.up() == adjacent:
            # If going up from original led to the outer grid then we are
            # interested in the point just above the middle
            point_of_interest = MIDDLE.up()
        elif original.down() == adjacent:
            # If going down from original led to the outer grid then we are
            # interested in the point just below the middle
            point_of_interest = MIDDLE.down()
        elif original.left() == adjacent:
            # If going left from original led to the outer grid then we are
            # interested in the point just to the left of the middle
            point_of_interest = MIDDLE.left()
        elif original.right() == adjacent:
            # If going right from original led to the outer grid then we are
            # interested in the point just to the right of the middle
            point_of_interest = MIDDLE.right()
        else:
            raise Exception('Unhandled adjacent point')
        return 1 if grid[point_of_interest] == ALIVE else 0

    def diversity(self):
        total = 0
        for grid in self.grids:
            total += sum([pow(2, self.to_index(point)) for point, value in grid.items() if value == ALIVE])
        return total

    def count_bugs(self):
        total = 0
        for grid in self.grids:
            total += sum([value == ALIVE for point, value in grid.items()])
        return total

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n\n'.join([str(grid) for grid in self.grids])

    @staticmethod
    def to_index(point):
        return (point.y() * 5) + point.x()


def main():
    # Part 1: 32776479
    print('Part 1: {}'.format(solve_part_1()))
    # Part 2: 2017
    print('Part 2: {}'.format(solve_part_2()))


def solve_part_1():
    seen = set()
    layout = Layout(get_grid(), False)
    while str(layout) not in seen:
        seen.add(str(layout))
        layout.step()
    return layout.diversity()


def solve_part_2():
    layout = Layout(get_grid(), True)
    for i in range(200):
        layout.step()
    return layout.count_bugs()


def get_grid():
    return Parser().as_grid()


if __name__ == '__main__':
    main()
