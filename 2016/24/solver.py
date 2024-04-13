import itertools
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser
from aoc.point import Point, PointHelper
from aoc.search import Search

WALL, OPEN = "#", "."


@dataclass(frozen=True)
class Marker:
    point: Point
    name: str


@dataclass(frozen=True)
class Grid:
    grid: dict[Point, str]

    def compute_distances(self) -> dict[tuple[str, str], int]:
        distances: dict[tuple[str, str], int] = dict()
        for start in self.get_markers():
            for end in self.get_markers():
                if start.name == end.name:
                    continue
                distance = distances.get((end.name, start.name))
                if distance is None:
                    search = Search[Point](
                        start=start.point,
                        end=end.point,
                        neighbors=self.get_adjacent,
                    )
                    distance = search.bfs()
                    assert distance is not None
                distances[(start.name, end.name)] = distance
        return distances

    def get_markers(self) -> list[Marker]:
        markers: list[Marker] = []
        for point, value in self.grid.items():
            if value not in [WALL, OPEN]:
                markers.append(Marker(point=point, name=value))
        return markers

    def get_adjacent(self, p: Point) -> list[Point]:
        result: list[Point] = []
        for adjacent in PointHelper.neighbors(p):
            if self.grid.get(adjacent, WALL) != WALL:
                result.append(adjacent)
        return result


@answer.timer
def main() -> None:
    distances = Grid(Parser().as_grid()).compute_distances()
    answer.part1(498, traverse(distances, False))
    answer.part2(804, traverse(distances, True))


def traverse(distances: dict[tuple[str, str], int], go_home: bool) -> int:
    shortest = None
    for permutation in generator(distances):
        permutation = list(permutation)
        if go_home:
            permutation.append("0")
        length = get_length(distances, permutation)
        if shortest is None or length < shortest:
            shortest = length
    assert shortest is not None
    return shortest


def generator(distances: dict[tuple[str, str], int]) -> list[tuple[str, ...]]:
    names = set([distance[0] for distance in distances])
    names.remove("0")
    return list(itertools.permutations(names))


def get_length(distances: dict[tuple[str, str], int], permutation: list[str]) -> int:
    total, previous = 0, "0"
    for current in permutation:
        total += distances[(previous, current)]
        previous = current
    return total


if __name__ == "__main__":
    main()
