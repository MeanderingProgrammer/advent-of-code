from dataclasses import dataclass, field

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int, int, int]


def diff(p1: Point, p2: Point) -> int:
    return sum([abs(p1[i] - p2[i]) for i in range(4)])


@dataclass(frozen=True)
class UnionFind:
    parents: dict[Point, Point] = field(default_factory=dict)
    ranks: dict[Point, int] = field(default_factory=dict)

    def run(self, points: list[Point]) -> int:
        for n in points:
            self.parents[n] = n
            self.ranks[n] = 1

        components = len(points)
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                p1, p2 = points[i], points[j]
                if diff(p1, p2) <= 3 and self.union(p1, p2):
                    components -= 1
        return components

    def union(self, n1: Point, n2: Point) -> bool:
        p1, p2 = self.find(n1), self.find(n2)
        if p1 == p2:
            return False
        r1, r2 = self.ranks[p1], self.ranks[p2]
        parent, child = (p1, p2) if r1 >= r2 else (p2, p1)
        self.parents[child] = parent
        self.ranks[parent] += self.ranks[child]
        return True

    def find(self, n: Point) -> Point:
        while self.parents[n] != n:
            n = self.parents[n]
        return n


@answer.timer
def main() -> None:
    answer.part1(375, UnionFind().run(get_points()))


def get_points() -> list[Point]:
    points: list[Point] = []
    for line in Parser().lines():
        x, y, z, w = line.split(",")
        point = (int(x), int(y), int(z), int(w))
        points.append(point)
    return points


if __name__ == "__main__":
    main()
