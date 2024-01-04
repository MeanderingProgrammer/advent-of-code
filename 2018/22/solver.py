import heapq
from dataclasses import dataclass
from typing import Optional, Self

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]


def neighbors(p: Point) -> list[Point]:
    return [(p[0] + dx, p[1] + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]


GEAR, TORCH, NEITHER = "g", "t", "n"
VALID_TOOL: dict[int, set[str]] = {
    0: set([GEAR, TORCH]),
    1: set([GEAR, NEITHER]),
    2: set([TORCH, NEITHER]),
}


@dataclass
class Region:
    depth: int
    target: Point
    location: Point
    left: Optional[Self]
    below: Optional[Self]
    cached_index: Optional[int] = None
    cached_erosion: Optional[int] = None

    def tools(self) -> set[str]:
        return VALID_TOOL[self.kind()]

    def kind(self) -> int:
        return self.erosion() % 3

    def erosion(self) -> int:
        if self.cached_erosion is None:
            self.cached_erosion = (self.index() + self.depth) % 20_183
        return self.cached_erosion

    def index(self) -> int:
        if self.cached_index is None:
            if self.location in [(0, 0), self.target]:
                self.cached_index = 0
            elif self.location[1] == 0:
                self.cached_index = self.location[0] * 16_807
            elif self.location[0] == 0:
                self.cached_index = self.location[1] * 48_271
            else:
                assert self.left is not None and self.below is not None
                self.cached_index = self.left.erosion() * self.below.erosion()
        return self.cached_index


Grid = dict[Point, Region]


@answer.timer
def main() -> None:
    lines = Parser().lines()
    parts = lines[1].split()[-1].split(",")
    target = (int(parts[0]), int(parts[1]))
    cave = build_out_cave(int(lines[0].split()[-1]), target)

    answer.part1(11575, risk_within(cave, target))
    answer.part2(1068, traverse(cave, (0, 0), target, TORCH))


def build_out_cave(depth: int, target: Point) -> Grid:
    grid, buff = dict(), 30
    for x in range(target[0] + 1 + buff):
        for y in range(target[1] + 1 + buff):
            location = (x, y)
            grid[location] = Region(
                depth, target, location, grid.get((x - 1, y)), grid.get((x, y - 1))
            )
    return grid


def risk_within(cave: Grid, target: Point) -> int:
    risk_levels = []
    for point, region in cave.items():
        if point[0] <= target[0] and point[1] <= target[1]:
            risk_levels.append(region.kind())
    return sum(risk_levels)


def traverse(cave: Grid, start: Point, end: Point, equipped: str) -> int:
    queue: list[tuple[int, tuple[Point, str]]] = []
    seen: set[tuple[Point, str]] = set()

    def add_item(time: int, location: Point, item: str) -> None:
        if (location, item) not in seen:
            heapq.heappush(queue, (time, (location, item)))

    add_item(0, start, equipped)
    while len(queue) > 0:
        time, (location, item) = heapq.heappop(queue)
        if (location, item) in seen:
            continue
        seen.add((location, item))
        if location == end and item == TORCH:
            return time
        elif location == end:
            add_item(time + 7, location, TORCH)
        else:
            for neighbor in neighbors(location):
                if neighbor not in cave:
                    continue
                if item in cave[neighbor].tools():
                    add_item(time + 1, neighbor, item)
                else:
                    for next_item in cave[neighbor].tools() & cave[location].tools():
                        add_item(time + 8, neighbor, next_item)
    raise Exception("Failed")


if __name__ == "__main__":
    main()
