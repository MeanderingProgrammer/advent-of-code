import itertools
from dataclasses import dataclass

from aoc import answer, search
from aoc.parser import Parser

Point = tuple[int, int]
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
                    distance = search.bfs(start.point, end.point, self.get_adjacent)
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
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            adjacent = (p[0] + dx, p[1] + dy)
            if adjacent in self.grid and self.grid[adjacent] != WALL:
                result.append(adjacent)
        return result


def main() -> None:
    distances = get_grid().compute_distances()
    answer.part1(498, traverse(distances, False))
    answer.part2(804, traverse(distances, True))


def get_grid() -> Grid:
    grid: dict[Point, str] = dict()
    for y, line in enumerate(Parser().lines()):
        for x, value in enumerate(line):
            grid[(x, y)] = value
    return Grid(grid)


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
