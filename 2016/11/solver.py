from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser
from aoc.search import Search


@dataclass(frozen=True)
class Floor:
    microchips: int
    generators: int

    @classmethod
    def new(cls, s: str) -> Self:
        # The first floor contains a plutonium generator, and a plutonium-compatible microchip.
        # -> ["a plutonium generator", "and a plutonium-compatible microchip"]
        items = s[:-1].split(" contains ")[1].split(", ")
        microchips, generators = 0, 0
        for item in items:
            # "and a plutonium-compatible microchip"
            # -> "microchip"
            part_type = item.split()[-1]
            if part_type == "microchip":
                microchips += 1
            else:
                assert part_type == "generator"
                generators += 1
        return cls(microchips, generators)

    def total(self) -> int:
        return self.microchips + self.generators

    def legal(self) -> bool:
        return self.generators == 0 or self.generators >= self.microchips

    def get_moves(self) -> list[Self]:
        result: list[Self] = []
        # Single microchip / generator
        if self.microchips >= 1:
            result.append(type(self)(microchips=1, generators=0))
        if self.generators >= 1:
            result.append(type(self)(microchips=0, generators=1))
        # Pair of microchips / generators
        if self.microchips >= 2:
            result.append(type(self)(microchips=2, generators=0))
        if self.generators >= 2:
            result.append(type(self)(microchips=0, generators=2))
        # Microchip / generator pair
        if self.microchips >= 1 and self.generators >= 1:
            result.append(type(self)(microchips=1, generators=1))
        return result

    def __add__(self, o: Self) -> Self:
        return type(self)(
            microchips=self.microchips + o.microchips,
            generators=self.generators + o.generators,
        )

    def __sub__(self, o: Self) -> Self:
        return type(self)(
            microchips=self.microchips - o.microchips,
            generators=self.generators - o.generators,
        )


@dataclass(frozen=True)
class State:
    level: int
    floors: tuple[Floor, ...]

    def none_below(self) -> bool:
        return sum([self.floors[level].total() for level in range(self.level)]) == 0

    def move(self, new_level: int, move: Floor) -> Self:
        new_floors: list[Floor] = []
        for level, floor in enumerate(self.floors):
            if level == self.level:
                new_floors.append(floor - move)
            elif level == new_level:
                new_floors.append(floor + move)
            else:
                new_floors.append(floor)
        return type(self)(level=new_level, floors=tuple(new_floors))

    def is_legal(self) -> bool:
        return all([floor.legal() for floor in self.floors])

    def __lt__(self, o: Self) -> bool:
        return self.floors[3].total() < o.floors[3].total()


@answer.timer
def main() -> None:
    lines = Parser().lines()

    floors: list[Floor] = []
    for line in lines[:-1]:
        floors.append(Floor.new(line))
    floors.append(Floor(0, 0))

    part1 = count_steps(floors)
    floors[0] += Floor(2, 2)
    part2 = count_steps(floors)

    answer.part1(37, part1)
    answer.part2(61, part2)


def count_steps(floors: list[Floor]) -> int | None:
    start = State(level=0, floors=tuple(floors))
    end = get_end_state(start)
    search = Search[State](
        start=start,
        end=end,
        neighbors=get_adjacent,
    )
    return search.dfs()


def get_end_state(start: State) -> State:
    last_floor = Floor(0, 0)
    for floor in start.floors:
        last_floor += floor
    floors: list[Floor] = [Floor(0, 0) for _ in range(3)]
    floors.append(last_floor)
    return State(level=3, floors=tuple(floors))


def get_adjacent(state: State) -> list[State]:
    moves = state.floors[state.level].get_moves()
    adjacent: list[State] = []
    for legal_state in get_legal(state, moves, False):
        adjacent.append(legal_state)
    for legal_state in get_legal(state, moves, True):
        adjacent.append(legal_state)
    return adjacent


def get_legal(state: State, moves: list[Floor], up: bool) -> list[State]:
    new_level = state.level + 1 if up else state.level - 1
    if new_level < 0 or new_level > 3:
        return []
    # If we are going down but there is nothing below then no point in moving things down
    if not up and state.none_below():
        return []
    if up:
        # If we're going upstairs and can carry 2 things don't bother carrying one
        prefer = [move for move in moves if move.total() == 2]
        moves = prefer if len(prefer) > 0 else moves
    else:
        # If we're going downstairs and can carry 1 thing don't bother carrying two
        prefer = [move for move in moves if move.total() == 1]
        moves = prefer if len(prefer) > 0 else moves
    legal: list[State] = []
    for move in moves:
        new_state = state.move(new_level, move)
        if new_state.is_legal():
            legal.append(new_state)
    return legal


if __name__ == "__main__":
    main()
