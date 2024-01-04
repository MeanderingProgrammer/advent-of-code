from aoc import answer
from aoc.board import Point
from aoc.parser import Parser


class PowerGrid:
    def __init__(self, serial_number: int, grid_size: int):
        self.serial_number = serial_number
        self.grid_size = grid_size
        self.grid = {}

    def initialize(self) -> None:
        for x in range(1, self.grid_size + 1):
            for y in range(1, self.grid_size + 1):
                point = Point(x, y)
                power_level = self.get_power_level(point)

                above = self.grid.get(Point(x, y - 1), 0)
                left = self.grid.get(Point(x - 1, y), 0)
                overlap = self.grid.get(Point(x - 1, y - 1), 0)

                self.grid[point] = above + left + power_level - overlap

    def get_largest_any(self) -> Point:
        largest_any = None
        for sub_grid_size in range(1, self.grid_size):
            largest = self.get_largest(sub_grid_size)
            if largest_any is None or largest[1] > largest_any[0][1]:
                largest_any = largest, sub_grid_size
        if largest_any is None:
            raise Exception("Should always be able to find largest grid")
        point = largest_any[0][0]
        return Point(point.x(), point.y(), largest_any[1])

    def get_largest(self, size: int) -> tuple[Point, int]:
        largest = None
        for x in range(1, self.grid_size - size + 1):
            for y in range(1, self.grid_size - size + 1):
                point = Point(x, y)
                power = self.get_total_power(point, size)
                if largest is None or power > largest[1]:
                    largest = point, power
        if largest is None:
            raise Exception("Should always be able to find largest sub grid")
        return largest

    def get_total_power(self, point: Point, size: int) -> int:
        total = self.grid[Point(point.x() + size - 1, point.y() + size - 1)]
        above = self.grid.get(Point(point.x() + size - 1, point.y() - 1), 0)
        left = self.grid.get(Point(point.x() - 1, point.y() + size - 1), 0)
        overlap = self.grid.get(Point(point.x() - 1, point.y() - 1), 0)
        return total - above - left + overlap

    def get_power_level(self, point: Point) -> int:
        rack_id = point.x() + 10
        initial_power_level = rack_id * point.y()
        power_level = initial_power_level + self.serial_number
        power_level *= rack_id
        power_level //= 100
        power_level %= 10
        return power_level - 5


@answer.timer
def main() -> None:
    power_grid = PowerGrid(Parser().integer(), 300)
    power_grid.initialize()
    answer.part1(Point(243, 43), power_grid.get_largest(3)[0])
    answer.part2(Point(236, 151, 15), power_grid.get_largest_any())


if __name__ == "__main__":
    main()
