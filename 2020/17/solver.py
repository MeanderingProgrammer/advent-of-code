from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Point:
    dimens: int
    coords: tuple[int, ...]

    def get_neighbors(self) -> list[Self]:
        neighbors: list[Self] = [self]
        for dimen in range(self.dimens):
            for i in range(len(neighbors)):
                coords: list[int] = list(neighbors[i].coords)
                coords[dimen] -= 1
                neighbors.append(type(self)(self.dimens, tuple(coords)))
                coords[dimen] += 2
                neighbors.append(type(self)(self.dimens, tuple(coords)))
        return neighbors[1:]


@dataclass
class Status:
    active: bool
    active_neighbors: int = 0

    def increment(self) -> None:
        self.active_neighbors += 1

    def update_state(self) -> None:
        if self.active:
            if self.active_neighbors not in [2, 3]:
                self.active = False
        else:
            if self.active_neighbors == 3:
                self.active = True
        self.active_neighbors = 0


@dataclass(frozen=True)
class Grid:
    grid: dict[Point, Status]

    def step(self) -> None:
        for point, status in list(self.grid.items()):
            if not status.active:
                continue
            for neighbor in point.get_neighbors():
                if neighbor not in self.grid:
                    self.grid[neighbor] = Status(active=False)
                self.grid[neighbor].increment()

        for status in self.grid.values():
            status.update_state()

    def get_active(self) -> int:
        return sum([status.active for status in self.grid.values()])


def main() -> None:
    answer.part1(284, simulate(3))
    answer.part2(2240, simulate(4))


def simulate(dimens: int) -> int:
    grid = get_grid(dimens)
    for _ in range(6):
        grid.step()
    return grid.get_active()


def get_grid(dimens: int) -> Grid:
    grid: dict[Point, Status] = dict()
    lines = Parser().lines()
    for y, line in enumerate(lines):
        y = len(lines) - y - 1
        for x, status in enumerate(line):
            grid[Point(dimens, (x, y, 0, 0))] = Status(active=status == "#")
    return Grid(grid=grid)


if __name__ == "__main__":
    main()
