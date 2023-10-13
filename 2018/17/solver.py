import sys
from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser

sys.setrecursionlimit(10_000)

CLAY = "#"
DOWN = "d"
LEFT = "l"
RIGHT = "r"


class PointRange:
    def __init__(self, raw):
        parts = raw.split(", ")
        coord_range = {}
        for part in parts:
            part = part.split("=")
            coord_range[part[0]] = self.get_range(part[1])
        self.xs = coord_range["x"]
        self.ys = coord_range["y"]

    def get_points(self):
        points = []
        for x in self.xs:
            for y in self.ys:
                point = Point(x, y)
                points.append(point)
        return points

    @staticmethod
    def get_range(values):
        values = values.split("..")
        if len(values) == 1:
            return [int(values[0])]
        elif len(values) == 2:
            return list(range(int(values[0]), int(values[1]) + 1))
        else:
            raise Exception("Can not handle such a range")


class GroundReservoir:
    def __init__(self, grid):
        self.grid = grid

        ys = list(self.grid.ys())[1:]
        self.min_y = min(ys)
        self.max_y = max(ys)

        self.flowing = set()
        self.settled = set()

    def fill(self, point, direction=DOWN):
        if self.grid[point] == CLAY:
            return True

        self.flowing.add(point)

        down = point.up()
        if not self.grid[down] == CLAY:
            if down not in self.flowing and self.in_range(down, False):
                self.fill(down)
            if down not in self.settled:
                return False

        left = point.left()
        right = point.right()

        left_filled = left not in self.flowing and self.fill(left, LEFT)
        right_filled = right not in self.flowing and self.fill(right, RIGHT)

        # All water at this 'level' has settled
        if direction == DOWN and left_filled and right_filled:
            self.settled.add(point)
            while left in self.flowing:
                self.settled.add(left)
                left = left.left()
            while right in self.flowing:
                self.settled.add(right)
                right = right.right()

        return (direction == LEFT and left_filled) or (
            direction == RIGHT and right_filled
        )

    def in_range(self, point, use_min=True):
        y = point.y()
        min_value = self.min_y if use_min else 1
        return y >= min_value and y <= self.max_y

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.grid)


def main():
    start = Point(500, 0)
    grid = get_grid()
    grid[start] = "."

    reservoir = GroundReservoir(grid)
    reservoir.fill(start)
    answer.part1(
        38409, len([point for point in reservoir.flowing if reservoir.in_range(point)])
    )
    answer.part2(
        32288, len([point for point in reservoir.settled if reservoir.in_range(point)])
    )


def get_grid():
    grid = Grid()
    for line in Parser().lines():
        point_range = PointRange(line)
        for point in point_range.get_points():
            grid[point] = CLAY
    return grid


if __name__ == "__main__":
    main()
