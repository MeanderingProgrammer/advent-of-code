from dataclasses import dataclass
from typing import Optional, override

from aoc import answer, search
from aoc.int_code import Bus, Computer
from aoc.parser import Parser

Point = tuple[int, int]


def add(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])


WALL, EMPTY, OXYGEN = 0, 1, 2
DIRECTIONS: dict[int, Point] = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
OPPOSITES: dict[int, int] = {1: 2, 2: 1, 3: 4, 4: 3}


class RepairDroid(Bus):
    def __init__(self):
        self.completed = False
        self.position: Point = (0, 0)
        self.next_position: Optional[tuple[int, Point]] = None
        self.path: list[tuple[int, Point]] = [(0, self.position)]
        self.grid: dict[Point, int] = {self.position: EMPTY}

    @override
    def active(self) -> bool:
        return not self.completed

    @override
    def get_input(self) -> Optional[int]:
        unexplored = self.get_unexplored()
        if unexplored is not None:
            self.next_position = unexplored
            return self.next_position[0]
        elif len(self.path) > 1:
            # If there is nowhere new to explore then we should go back
            previous = self.path[-1]
            self.next_position = self.path[-2]
            self.path = self.path[:-2]
            return OPPOSITES[previous[0]]
        else:
            self.completed = True

    def get_unexplored(self) -> Optional[tuple[int, Point]]:
        for code, direction in DIRECTIONS.items():
            next_position = add(self.position, direction)
            if next_position not in self.grid:
                return code, next_position
        return None

    @override
    def add_output(self, value: int) -> None:
        # Make sure we can identify the input
        assert value in [WALL, EMPTY, OXYGEN], f"Unexpected status code: {value}"
        assert self.next_position is not None
        next_position = self.next_position[1]
        self.grid[next_position] = value
        # If we can move to the given position then go
        if value in [EMPTY, OXYGEN]:
            self.position = next_position
            self.path.append(self.next_position)


@dataclass(frozen=True)
class Traverser:
    grid: dict[Point, int]

    def min_steps(self, position: Point) -> int:
        min_path = search.bfs_complete(
            start=(0, position),
            is_done=lambda current: self.grid[current] == OXYGEN,
            get_adjacent=self.get_options,
        )
        assert min_path is not None
        return min_path

    def get_options(self, position: Point) -> list[tuple[int, Point]]:
        options: list[tuple[int, Point]] = []
        for direction in DIRECTIONS.values():
            next_position = add(position, direction)
            if self.grid.get(next_position, WALL) != WALL:
                options.append((1, next_position))
        return options

    def empty_locations(self) -> list[Point]:
        return [location for location, value in self.grid.items() if value == EMPTY]


@answer.timer
def main() -> None:
    droid = RepairDroid()
    Computer(bus=droid, memory=Parser().int_csv()).run()
    traverser = Traverser(grid=droid.grid)
    answer.part1(224, traverser.min_steps((0, 0)))
    answer.part2(284, time_for_air(traverser))


def time_for_air(traverser: Traverser) -> int:
    steps_needed = [
        traverser.min_steps(position) for position in traverser.empty_locations()
    ]
    return max(steps_needed)


if __name__ == "__main__":
    main()
