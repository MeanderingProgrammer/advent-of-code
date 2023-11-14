from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]
DIRECTIONS: dict[str, Point] = dict(
    e=(2, 0),
    w=(-2, 0),
    ne=(1, 1),
    nw=(-1, 1),
    se=(1, -1),
    sw=(-1, -1),
)


def add(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])


def neighbors(p: Point) -> list[Point]:
    return [add(p, direction) for direction in DIRECTIONS.values()]


class Path:
    def __init__(self, path: str):
        self.instructions: list[Point] = []
        path_iter = iter(path)
        for letter in path_iter:
            instruction = letter if letter in ["e", "w"] else letter + next(path_iter)
            self.instructions.append(DIRECTIONS[instruction])


@dataclass(frozen=True)
class Floor:
    floor: dict[Point, bool]

    def follow_path(self, path: Path) -> None:
        point = (0, 0)
        for instruction in path.instructions:
            point = add(point, instruction)
            if point not in self.floor:
                self.floor[point] = True
        self.flip(point)

    def transform(self) -> None:
        self.pad_around_black()
        to_flip: list[Point] = []
        for point, tile in self.floor.items():
            flip_counts = [2] if tile else [0, 3, 4, 5, 6]
            black_count = sum(
                [not self.floor.get(neighbor, True) for neighbor in neighbors(point)]
            )
            if black_count in flip_counts:
                to_flip.append(point)
        [self.flip(point) for point in to_flip]

    def pad_around_black(self) -> None:
        for point in list(self.floor.keys()):
            if self.floor[point]:
                continue
            for neighbor in neighbors(point):
                if neighbor in self.floor:
                    continue
                self.floor[neighbor] = True

    def flip(self, point: Point) -> None:
        self.floor[point] = not self.floor[point]

    def count_black(self):
        return sum([not tile for tile in self.floor.values()])


def main() -> None:
    floor = Floor(floor={(0, 0): True})
    paths = [Path(line) for line in Parser().lines()]
    for path in paths:
        floor.follow_path(path)
    answer.part1(320, floor.count_black())
    for _ in range(100):
        floor.transform()
    answer.part2(3777, floor.count_black())


if __name__ == "__main__":
    main()
