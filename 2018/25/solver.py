from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int, int, int]


def diff(p1: Point, p2: Point) -> int:
    return sum([abs(p1[i] - p2[i]) for i in range(4)])


@dataclass(frozen=True)
class Constallation:
    points: set[Point]

    def add(self, points: list[Point]) -> None:
        [self.points.add(point) for point in points]

    def fits(self, p: Point) -> bool:
        for point in self.points:
            if diff(point, p) <= 3:
                return True
        return False


def main() -> None:
    constallations: list[Constallation] = []
    for point in get_points():
        options = get_options(point, constallations)
        if len(options) == 0:
            constallations.append(Constallation(points=set([point])))
        elif len(options) == 1:
            options[0].add([point])
        else:
            to_delete = merge(point, options)
            for option in to_delete:
                constallations.remove(option)
    answer.part1(375, len(constallations))


def get_points() -> list[Point]:
    points: list[Point] = []
    for line in Parser().lines():
        x, y, z, w = line.split(",")
        point = (int(x), int(y), int(z), int(w))
        points.append(point)
    return points


def get_options(
    point: Point, constallations: list[Constallation]
) -> list[Constallation]:
    options: list[Constallation] = []
    for constallation in constallations:
        if constallation.fits(point):
            options.append(constallation)
    return options


def merge(point: Point, options: list[Constallation]):
    merged: Constallation = options[0]
    merged.add([point])
    to_delete = options[1:]
    for constallation in to_delete:
        merged.add(list(constallation.points))
    return to_delete


if __name__ == "__main__":
    main()
