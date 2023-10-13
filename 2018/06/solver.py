from aoc import answer
from aoc.board import Point
from aoc.parser import Parser
from collections import defaultdict
from typing import Dict, List, Optional


class PointGrid:
    def __init__(self, points: List[Point]):
        self.points = points

        xs = [point.x() for point in points]
        self.min_x: int = min(xs)
        self.max_x: int = max(xs)

        ys = [point.y() for point in points]
        self.min_y: int = min(ys)
        self.max_y: int = max(ys)

        self.distances: Dict[Point, Dict[Point, int]] = {}
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                start = Point(x, y)
                self.distances[start] = {end: len(start - end) for end in self.points}

    def largest_finite(self) -> int:
        point_to_closest = defaultdict(list)
        for point, distances in self.distances.items():
            closest = self.get_closest(distances)
            if closest is not None:
                point_to_closest[closest].append(point)

        finite_sizes = []
        for closest in point_to_closest.values():
            if self.is_finite(closest):
                finite_sizes.append(len(closest))
        return max(finite_sizes)

    def get_closest(self, distances: Dict[Point, int]) -> Optional[Point]:
        min_distance = min(distances.values())
        closest_points = []
        for option, distance in distances.items():
            if distance == min_distance:
                closest_points.append(option)
        return closest_points[0] if len(closest_points) == 1 else None

    def is_finite(self, closest: List[Point]) -> bool:
        x_boundary = [self.min_x, self.min_y]
        y_boundary = [self.min_y, self.max_y]
        for point in closest:
            if point.x() in x_boundary or point.y() in y_boundary:
                return False
        return True

    def within_max_distance(self, max_distance: int) -> int:
        # Assumes no points outside of min / max boundaries fall within the
        # max allowable distance, this assumption could be checked
        contained = [
            sum(distances.values()) < max_distance
            for distances in self.distances.values()
        ]
        return sum(contained)


def main():
    point_grid = get_point_grid()
    answer.part1(3251, point_grid.largest_finite())
    answer.part2(47841, point_grid.within_max_distance(10_000))


def get_point_grid() -> PointGrid:
    points = []
    for line in Parser().lines():
        parts = line.split(", ")
        point = Point(int(parts[0]), int(parts[1]))
        points.append(point)
    return PointGrid(points)


if __name__ == "__main__":
    main()
