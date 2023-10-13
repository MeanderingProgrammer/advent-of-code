from aoc import answer
from aoc.parser import Parser


class Tile:
    def __init__(self):
        self.color = "w"

    def flip(self):
        self.color = "w" if self.is_black() else "b"

    def is_black(self):
        return self.color == "b"

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.directions = {
            "e": (2, 0),
            "w": (-2, 0),
            "ne": (1, 1),
            "nw": (-1, 1),
            "se": (1, -1),
            "sw": (-1, -1),
        }

    def go(self, instruction):
        direction = self.directions[instruction]
        return Point(self.x + direction[0], self.y + direction[1])

    def get_adjacent(self):
        adjacent = []
        for direction in self.directions.values():
            adjacent.append(self + direction)
        return adjacent

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Floor:
    def __init__(self):
        self.floor = {}
        self.floor[Point(0, 0)] = Tile()

    def follow_path(self, path):
        point = Point(0, 0)
        for instruction in path.instructions:
            point = point.go(instruction)
            if point not in self.floor:
                self.floor[point] = Tile()
        return self.floor[point]

    def transform(self):
        self.pad_around_black()

        to_flip = []
        for point in self.floor:
            tile = self.floor[point]
            are_black = [
                self.floor.get(adjacent_point, Tile()).is_black()
                for adjacent_point in point.get_adjacent()
            ]
            black_count = sum(are_black)

            if tile.is_black():
                if black_count == 0 or black_count > 2:
                    to_flip.append(tile)
            else:
                if black_count == 2:
                    to_flip.append(tile)

        for tile in to_flip:
            tile.flip()

    def pad_around_black(self):
        points = list(self.floor.keys())
        for point in points:
            if self.floor[point].is_black():
                for adjacent_point in point.get_adjacent():
                    if adjacent_point not in self.floor:
                        self.floor[adjacent_point] = Tile()

    def count_black_tiles(self):
        is_black = [tile.is_black() for tile in self.floor.values()]
        return sum(is_black)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.floor)


class Path:
    def __init__(self, path):
        self.instructions = []
        it = iter(path)
        for letter in it:
            instruction = letter if letter in ["e", "w"] else letter + next(it)
            self.instructions.append(instruction)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.instructions)


def main():
    floor = Floor()
    paths = get_paths()

    for path in paths:
        floor.follow_path(path).flip()
    answer.part1(320, floor.count_black_tiles())

    days = 100
    for day in range(days):
        floor.transform()
    answer.part2(3777, floor.count_black_tiles())


def get_paths():
    return [Path(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
