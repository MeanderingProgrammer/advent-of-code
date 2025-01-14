from dataclasses import dataclass
from typing import Callable

from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser


def neighbors(dimens: int) -> list[list[int]]:
    result: list[list[int]] = [[]]
    for _ in range(dimens):
        next: list[list[int]] = []
        for values in result:
            for value in [-1, 0, 1]:
                next.append(values + [value])
        result = next
    mid = len(result) // 2
    return result[:mid] + result[mid + 1 :]


type Point3d = tuple[int, int, int]
neighbors_3d = neighbors(3)


def get_neighbors_3d(p: Point3d) -> list[Point3d]:
    result: list[Point3d] = []
    for x, y, z in neighbors_3d:
        result.append((p[0] + x, p[1] + y, p[2] + z))
    return result


type Point4d = tuple[int, int, int, int]
neighbors_4d = neighbors(4)


def get_neighbors_4d(p: Point4d) -> list[Point4d]:
    result: list[Point4d] = []
    for w, x, y, z in neighbors_4d:
        result.append((p[0] + w, p[1] + x, p[2] + y, p[3] + z))
    return result


@dataclass
class Status:
    active: bool = False
    active_neighbors: int = 0

    def increment(self) -> None:
        self.active_neighbors += 1

    def update(self) -> None:
        if self.active:
            if self.active_neighbors not in [2, 3]:
                self.active = False
        else:
            if self.active_neighbors == 3:
                self.active = True
        self.active_neighbors = 0


@dataclass(frozen=True)
class State[T]:
    items: dict[T, Status]
    neighbors: Callable[[T], list[T]]

    def step(self) -> None:
        for point, status in list(self.items.items()):
            if not status.active:
                continue
            for neighbor in self.neighbors(point):
                if neighbor not in self.items:
                    self.items[neighbor] = Status()
                self.items[neighbor].increment()
        for status in self.items.values():
            status.update()

    def get_active(self) -> int:
        return sum([status.active for status in self.items.values()])


@answer.timer
def main() -> None:
    grid = Parser().as_grid()
    answer.part1(284, simulate(as_3d(grid)))
    answer.part2(2240, simulate(as_4d(grid)))


def simulate(state: State) -> int:
    for _ in range(6):
        state.step()
    return state.get_active()


def as_3d(grid: Grid[str]) -> State[Point3d]:
    items: dict[Point3d, Status] = dict()
    for (x, y), status in grid.items():
        items[(x, y, 0)] = Status(active=status == "#")
    return State(items=items, neighbors=get_neighbors_3d)


def as_4d(grid: Grid[str]) -> State[Point4d]:
    items: dict[Point4d, Status] = dict()
    for (x, y), status in grid.items():
        items[(x, y, 0, 0)] = Status(active=status == "#")
    return State(items=items, neighbors=get_neighbors_4d)


if __name__ == "__main__":
    main()
