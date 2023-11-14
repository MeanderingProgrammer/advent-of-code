from typing import Optional, override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser

Point = tuple[int, int]


def add(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])


WALL, EMPTY, OXYGEN_SYSTEM = 0, 1, 2
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
        if len(unexplored) > 0:
            self.next_position = unexplored[0]
            return self.next_position[0]
        elif len(self.path) > 1:
            # If there is nowhere new to explore then we should go back
            previous = self.path[-1]
            self.next_position = self.path[-2]
            self.path = self.path[:-2]
            return OPPOSITES[previous[0]]
        else:
            self.completed = True

    @override
    def add_output(self, status: int) -> None:
        # Make sure we can identify the status code
        if status not in [WALL, EMPTY, OXYGEN_SYSTEM]:
            raise Exception(f"Unexpected status code: {status}")
        assert self.next_position is not None
        next_position = self.next_position[1]
        # No matter the status we now know something about the new position
        self.grid[next_position] = status
        # If we can move to the given position then go
        if status in [EMPTY, OXYGEN_SYSTEM]:
            self.position = next_position
            self.path.append(self.next_position)

    def get_empty_locations(self) -> list[Point]:
        return [location for location in self.grid if self.grid[location] == EMPTY]

    def get_min_steps(self, position: Point) -> int:
        path = [position]
        min_path = self.get_path(position, path)
        assert min_path is not None
        return len(min_path) - 1

    def get_path(self, position: Point, path: list[Point]) -> Optional[list[Point]]:
        if self.grid.get(position, EMPTY) == OXYGEN_SYSTEM:
            return path
        options = self.get_options(position)
        options = [option for option in options if option not in path]
        min_path = None
        for option in options:
            result = self.get_path(option, path + [option])
            if result is not None:
                if min_path is None or len(result) < len(min_path):
                    min_path = result
        return min_path

    def get_unexplored(self) -> list[tuple[int, Point]]:
        unexplored = []
        for code, direction in DIRECTIONS.items():
            next_position = add(self.position, direction)
            if next_position not in self.grid:
                unexplored.append((code, next_position))
        return unexplored

    def get_options(self, position: Point) -> list[Point]:
        options = []
        for direction in DIRECTIONS.values():
            next_position = add(position, direction)
            if self.grid.get(next_position, WALL) != WALL:
                options.append(next_position)
        return options


def main() -> None:
    droid = RepairDroid()
    Computer(bus=droid, memory=Parser().int_csv()).run()
    answer.part1(224, droid.get_min_steps((0, 0)))
    answer.part2(284, time_for_air(droid))


def time_for_air(droid: RepairDroid) -> int:
    # Can optimize by storing optimal paths in cache since we
    # know all subpaths lengths
    steps_needed = []
    for empty_location in droid.get_empty_locations():
        steps_needed.append(droid.get_min_steps(empty_location))
    return max(steps_needed)


if __name__ == "__main__":
    main()
