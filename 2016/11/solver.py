import itertools
from dataclasses import dataclass
from typing import Optional, Self

from aoc import answer, search
from aoc.parser import Parser

type Item = tuple[str, bool]


def to_generator(item: Item) -> Item:
    assert item[1], "Can only get generator for a chip"
    return (item[0], False)


@dataclass
class State:
    state: list[set[Item]]
    hashed: Optional[int] = None
    equalized: Optional[list[set[str]]] = None

    def total_below(self, floor: int) -> int:
        return sum([len(self.state[level]) for level in range(floor)])

    def move(self, new_level: int, items_to_move: tuple[Item, ...]) -> Self:
        new_state: list[set[Item]] = [set() for _ in range(4)]
        for floor, items in enumerate(self.state):
            for item in items:
                if item not in items_to_move:
                    new_state[floor].add(item)
        for item in items_to_move:
            new_state[new_level].add(item)
        return type(self)(state=new_state)

    def is_legal(self, floors: list[int]) -> bool:
        for floor in floors:
            if self.contains_unpaired_chip(floor):
                return False
        return True

    def contains_unpaired_chip(self, floor: int) -> bool:
        items = self.state[floor]
        chips = [item for item in items if item[1]]
        generators = [item for item in items if not item[1]]
        if len(chips) == 0 or len(generators) == 0:
            return False
        for chip in chips:
            if to_generator(chip) not in generators:
                return True
        return False

    def _get_floor(self, target: Item) -> int:
        for i, items in enumerate(self.state):
            for item in items:
                if item == target:
                    return i
        raise Exception(f"Could not find item: {target}")

    def _equalize(self) -> list[set[str]]:
        if self.equalized is None:
            result: list[set[str]] = [set() for _ in range(4)]
            item_index = 0
            for floor, items in enumerate(self.state):
                for item in items:
                    if item[1]:
                        result[floor].add(f"{item_index}C")
                        generator_floor = self._get_floor(to_generator(item))
                        result[generator_floor].add(f"{item_index}G")
                        item_index += 1
            self.equalized = result
        return self.equalized

    def __eq__(self, o) -> bool:
        return self._equalize() == o._equalize()

    def __hash__(self) -> int:
        if self.hashed is None:
            result = []
            for items in self._equalize():
                result.append(frozenset(items))
            self.hashed = hash(frozenset(result))
        return self.hashed

    def __lt__(self, o: Self) -> bool:
        return len(self.state[3]) < len(o.state[3])


@answer.timer
def main() -> None:
    answer.part1(37, count_steps([]))
    additional_items = [
        "elerium generator",
        "elerium-compatible microchip",
        "dilithium generator",
        "dilithium-compatible microchip",
    ]
    answer.part2(61, count_steps(additional_items))


def count_steps(additional_items: list[str]) -> Optional[int]:
    start = get_start_state(additional_items)
    end = get_end_state(start)
    return search.bfs((0, start), (3, end), get_adjacent)


def get_start_state(additional_items: list[str]) -> State:
    def parse_items(line: str, add_additional: bool) -> set[Item]:
        # The first floor contains a plutonium generator, and a plutonium-compatible microchip.
        # ["a plutonium generator", "and a plutonium-compatible microchip"]
        items = line[:-1].split(" contains ")[1].split(", ")
        if add_additional:
            items += additional_items
        result: set[Item] = set()
        for raw_item in items:
            parts = raw_item.split()
            item: Item = (
                parts[-2].split("-")[0],
                parts[-1] == "microchip",
            )
            result.add(item)
        return result

    state: list[set[Item]] = []
    # Remove: The fourth floor contains nothing relevant.
    for i, line in enumerate(Parser().lines()[:-1]):
        items = parse_items(line, i == 0)
        state.append(items)
    state.append(set())
    return State(state=state)


def get_end_state(start: State) -> State:
    state: list[set[Item]] = [set() for _ in range(4)]
    for items in start.state:
        state[3].update(items)
    return State(state=state)


def get_adjacent(item: tuple[int, State]) -> list[tuple[int, State]]:
    level, state = item
    options = get_options(state.state[level])
    adjacent: list[tuple[int, State]] = []
    for legal_state in get_legal(level, state, options, False):
        adjacent.append((level - 1, legal_state))
    for legal_state in get_legal(level, state, options, True):
        adjacent.append((level + 1, legal_state))
    return adjacent


def get_options(items: set[Item]) -> list[tuple[Item, ...]]:
    result: list[tuple[Item, ...]] = []
    # Any singular item
    for item in items:
        result.append((item,))
    # Any pair of microcips
    chips = [item for item in items if item[1]]
    for pair in itertools.combinations(chips, 2):
        result.append(pair)
    # Any pair of generators
    generators = [item for item in items if not item[1]]
    for pair in itertools.combinations(generators, 2):
        result.append(pair)
    # Some pair of matching chip and generator, all are equivalent
    matching_pair = get_matching_pair(chips, generators)
    if matching_pair is not None:
        result.append(matching_pair)
    return result


def get_matching_pair(
    chips: list[Item], generators: list[Item]
) -> Optional[tuple[Item, ...]]:
    for chip in chips:
        for generator in generators:
            if chip[0] == generator[0]:
                return (chip, generator)
    return None


def get_legal(
    start_level: int, state: State, options: list[tuple[Item, ...]], up: bool
) -> set[State]:
    new_level = start_level + 1 if up else start_level - 1
    if new_level < 0 or new_level > 3:
        return set()

    # If we are going down but there is nothing below there is no point in moving things down
    if not up and state.total_below(start_level) == 0:
        return set()

    carry_1 = [option for option in options if len(option) == 1]
    carry_2 = [option for option in options if len(option) == 2]
    if up:
        # If we're going upstairs and can carry 2 things don't bother carrying one
        options = carry_2 if len(carry_2) > 0 else carry_1
    else:
        # If we're going downstairs and can carry 1 thing don't bother carrying two
        options = carry_1 if len(carry_1) > 0 else carry_2

    legal: set[State] = set()
    for option in options:
        new_state = state.move(new_level, option)
        if new_state.is_legal([start_level, new_level]):
            legal.add(new_state)
    return legal


if __name__ == "__main__":
    main()
