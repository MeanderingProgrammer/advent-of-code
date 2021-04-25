from commons.aoc_board import Grid, Point
from commons.aoc_parser import Parser


class Animator:

    def __init__(self, force_corners, on, min_x, max_x, min_y, max_y):
        self.force_corners = force_corners
        self.on = on

        self.min_x = min_x
        self.max_x = max_x

        self.min_y = min_y
        self.max_y = max_y

        self.add_corners()

    def add_corners(self):
        if self.force_corners:
            self.on.add(Point(self.min_x, self.min_y))
            self.on.add(Point(self.min_x, self.max_y))
            self.on.add(Point(self.max_x, self.min_y))
            self.on.add(Point(self.max_x, self.max_y))

    def step(self):
        next_on = set()

        for point in self.get_points():
            neighbors_on = self.neighbors_on(point)
            neighbors_needed = [2, 3] if point in self.on else [3]
            if neighbors_on in neighbors_needed:
                next_on.add(point)

        self.on = next_on
        self.add_corners()

    def get_points(self):
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                yield Point(x, y)

    def neighbors_on(self, point):
        return sum([adjacent in self.on for adjacent in point.adjacent(True)])

    def lights_on(self):
        return len(self.on)


def main():
    grid = Parser().as_grid()

    # Part 1: 1061
    print('Part 1: {}'.format(run(False, grid)))
    # Part 2: 1006
    print('Part 2: {}'.format(run(True, grid)))


def run(force_corners, grid):
    on = points_on(grid)
    min_x, max_x = min_max(grid.xs())
    min_y, max_y = min_max(grid.ys())

    animator = Animator(force_corners, on, min_x, max_x, min_y, max_y)
    for i in range(100):
        animator.step()
    return animator.lights_on()


def points_on(grid):
    on = set()
    for point, value in grid.items():
        if value == '#':
            on.add(point)
    return on


def min_max(values):
    return min(values), max(values)


if __name__ == '__main__':
    main()
