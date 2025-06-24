from dataclasses import dataclass, field
from typing import override

from aoc import answer
from aoc.grid import Grid
from aoc.int_code import Bus, Computer
from aoc.parser import Parser
from aoc.point import Point, PointHelper

WALL, EMPTY, OXYGEN = 0, 1, 2
DIRECTIONS: dict[int, Point] = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
OPPOSITES: dict[int, int] = {1: 2, 2: 1, 3: 4, 4: 3}


@dataclass
class RepairDroid(Bus):
    completed: bool = False
    position: Point = (0, 0)
    next_position: tuple[int, Point] | None = None
    path: list[tuple[int, Point]] = field(default_factory=lambda: [(0, (0, 0))])
    grid: Grid[int] = field(default_factory=lambda: {(0, 0): EMPTY})

    @override
    def active(self) -> bool:
        return not self.completed

    @override
    def get_input(self) -> int:
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
            return 0

    def get_unexplored(self) -> tuple[int, Point] | None:
        for code, direction in DIRECTIONS.items():
            next_position = PointHelper.add(self.position, direction)
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
    grid: Grid[int]

    def bfs(self, start: Point) -> int:
        queue: list[tuple[int, Point]] = [(0, start)]
        seen: set[Point] = set()
        while len(queue) > 0:
            minutes, position = queue.pop(0)
            if position in seen:
                continue
            seen.add(position)
            if self.grid[position] == OXYGEN:
                return minutes
            for next_position in PointHelper.neighbors(position):
                if self.grid.get(next_position, WALL) != WALL:
                    if next_position not in seen:
                        queue.append((minutes + 1, next_position))
        raise Exception("No path found")

    def time_for_air(self) -> int:
        empty = [location for location, value in self.grid.items() if value == EMPTY]
        steps_needed = [self.bfs(position) for position in empty]
        return max(steps_needed)


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    droid = RepairDroid()
    Computer(bus=droid, memory=memory).run()
    traverser = Traverser(grid=droid.grid)
    answer.part1(224, traverser.bfs((0, 0)))
    answer.part2(284, traverser.time_for_air())


if __name__ == "__main__":
    main()
