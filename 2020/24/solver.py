from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser
from aoc.point import Point, PointHelper

DIRECTIONS: dict[str, Point] = dict(
    e=(2, 0),
    w=(-2, 0),
    ne=(1, 1),
    nw=(-1, 1),
    se=(1, -1),
    sw=(-1, -1),
)


def neighbors(p: Point) -> list[Point]:
    return [PointHelper.add(p, direction) for direction in DIRECTIONS.values()]


@dataclass(frozen=True)
class Floor:
    floor: dict[Point, bool]

    def follow_path(self, path: str) -> None:
        point: Point = (0, 0)
        path_iter = iter(path)
        for letter in path_iter:
            instruction = letter if letter in ["e", "w"] else letter + next(path_iter)
            point = PointHelper.add(point, DIRECTIONS[instruction])
        self.floor[point] = not self.get(point)

    def transform(self) -> None:
        # Track number of black tiles adjacent to every point on the floor
        counts: dict[Point, int] = dict()
        for point, tile in self.floor.items():
            counts[point] = counts.get(point, 0)
            if not tile:
                for neighbor in neighbors(point):
                    counts[neighbor] = counts.get(neighbor, 0) + 1
        # Flip tiles depending on current state and number of adjacent black tiles
        for point, count in counts.items():
            tile = self.get(point)
            flip_counts = [2] if tile else [0, 3, 4, 5, 6]
            if count in flip_counts:
                self.floor[point] = not tile

    def get(self, point: Point) -> bool:
        return self.floor.get(point, True)

    def count_black(self):
        return sum([not tile for tile in self.floor.values()])


@answer.timer
def main() -> None:
    floor = Floor(dict())
    for path in Parser().lines():
        floor.follow_path(path)
    answer.part1(320, floor.count_black())
    for _ in range(100):
        floor.transform()
    answer.part2(3777, floor.count_black())


if __name__ == "__main__":
    main()
