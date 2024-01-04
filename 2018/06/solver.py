from collections import defaultdict
from typing import Optional

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]


def distance(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class PointGrid:
    def __init__(self, points: list[Point]):
        xs = [point[0] for point in points]
        self.x_bounds: tuple[int, int] = min(xs), max(xs)

        ys = [point[1] for point in points]
        self.y_bounds: tuple[int, int] = min(ys), max(ys)

        self.distances: dict[Point, dict[Point, int]] = dict()
        for x in range(self.x_bounds[0], self.x_bounds[1] + 1):
            for y in range(self.y_bounds[0], self.y_bounds[1] + 1):
                start = (x, y)
                self.distances[start] = {end: distance(start, end) for end in points}

    def largest_finite(self) -> int:
        regions = defaultdict(list)
        for point in self.distances:
            closest = self.get_closest(point)
            if closest is not None:
                regions[closest].append(point)
        finite = [cluster for cluster in regions.values() if self.finite(cluster)]
        return max([len(cluster) for cluster in finite])

    def get_closest(self, point: Point) -> Optional[Point]:
        distances = self.distances[point]
        min_distance = min(distances.values())
        points = list(filter(lambda p: distances[p] == min_distance, distances))
        return points[0] if len(points) == 1 else None

    def finite(self, cluster: list[Point]) -> bool:
        return all(
            [x not in self.x_bounds and y not in self.y_bounds for x, y in cluster]
        )

    def within_distance(self, distance: int) -> int:
        # Assumes no points outside of min / max boundaries fall within the
        # max allowable distance, this assumption could be checked
        contained = [
            sum(distances.values()) < distance for distances in self.distances.values()
        ]
        return sum(contained)


@answer.timer
def main() -> None:
    point_grid = get_point_grid()
    answer.part1(3251, point_grid.largest_finite())
    answer.part2(47841, point_grid.within_distance(10_000))


def get_point_grid() -> PointGrid:
    points: list[Point] = []
    for line in Parser().lines():
        x, y = line.split(", ")
        points.append((int(x), int(y)))
    return PointGrid(points)


if __name__ == "__main__":
    main()
