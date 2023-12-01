import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def angle(self, other: Self) -> float:
        dy = other.y - self.y
        dx = other.x - self.x
        # Correct for inverted y coordinates
        angle = math.degrees(math.atan2(-dy, dx))
        # Correct for 0 degrees being at top
        angle -= 90
        # Correct for negative values and flipped direction
        return -angle if angle <= 0 else 360 - angle

    def distance(self, other: Self) -> float:
        dy = self.y - other.y
        dx = self.x - other.x
        return pow(pow(dx, 2) + pow(dy, 2), 0.5)


class Grid:
    def __init__(self, data: list[str]):
        self.asteroids = []
        for y, row in enumerate(data):
            for x, value in enumerate(row):
                if value == "#":
                    self.asteroids.append(Point(x, y))

    def get_most_seen(self) -> tuple[Point, int]:
        asteroid_angles = [self.get_angles(asteroid) for asteroid in self.asteroids]
        unique_counts = [len(asteroid) for asteroid in asteroid_angles]
        max_count = max(unique_counts)
        asteroid_index = unique_counts.index(max_count)
        return self.asteroids[asteroid_index], max_count

    def get_destruction_order(self, location: Point) -> list[Point]:
        angles = self.get_angles(location)
        destruction_order: list[Point] = []
        for angle in sorted(list(angles)):
            asteroids = angles[angle]
            distances = [location.distance(asteroid) for asteroid in asteroids]
            asteroid = asteroids[distances.index(min(distances))]
            destruction_order.append(asteroid)
        return destruction_order

    def get_angles(self, start: Point) -> dict[float, list[Point]]:
        angles = defaultdict(list)
        [angles[start.angle(end)].append(end) for end in self.asteroids if end != start]
        return angles


def main() -> None:
    grid = Grid(Parser().lines())
    asteroid, count = grid.get_most_seen()
    answer.part1(230, count)
    asteroid = grid.get_destruction_order(asteroid)[199]
    answer.part2(1205, (asteroid.x * 100) + asteroid.y)


if __name__ == "__main__":
    main()
