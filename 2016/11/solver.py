import itertools
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Self

from aoc import answer, search
from aoc.parser import Parser


class ItemType(Enum):
    CHIP = 1
    GENERATOR = 2


@dataclass(frozen=True)
class Item:
    element: str
    item_type: ItemType

    def generator(self) -> Self:
        if self.item_type == ItemType.GENERATOR:
            raise Exception("Cannot get generator for a generator")
        return type(self)(self.element, ItemType.GENERATOR)


class State:
    def __init__(self):
        # 4 floors with nothing on at first
        self.state: dict[int, set[Item]] = {i: set() for i in range(4)}
        self.hashed = None
        self.equalized = None

    def add(self, floor: int, item: Item) -> None:
        self.state[floor].add(item)

    def get(self, floor: int) -> set[Item]:
        return self.state[floor]

    def total_below(self, floor: int) -> int:
        return sum([len(self.state[level]) for level in range(floor)])

    def move(self, new_level: int, items_to_move: list[Item]) -> Self:
        new_state = type(self)()
        for floor, items in self.state.items():
            for item in items:
                if item not in items_to_move:
                    new_state.add(floor, item)
        for item in items_to_move:
            new_state.add(new_level, item)
        return new_state

    def is_legal(self, floors: list[int]) -> bool:
        for floor in floors:
            if self.contains_unpaired_chip(floor):
                return False
        return True

    def contains_unpaired_chip(self, floor: int) -> bool:
        items = self.get(floor)
        chips = [item for item in items if item.item_type == ItemType.CHIP]
        generators = [item for item in items if item.item_type == ItemType.GENERATOR]
        if len(chips) == 0 or len(generators) == 0:
            return False
        for chip in chips:
            if chip.generator() not in generators:
                return True
        return False

    def _get_floor(self, target: Item) -> int:
        for i, items in self.state.items():
            for item in items:
                if item == target:
                    return i
        raise Exception(f"Could not find item: {target}")

    def _equalize(self) -> dict[int, set[str]]:
        if self.equalized is None:
            result: dict[int, set[str]] = {i: set() for i in range(4)}
            item_index = 0
            for floor, items in self.state.items():
                for item in items:
                    if item.item_type == ItemType.CHIP:
                        result[floor].add(f"{item_index}C")
                        generator_floor = self._get_floor(item.generator())
                        result[generator_floor].add(f"{item_index}G")
                        item_index += 1
            self.equalized = result
        return self.equalized

    def __eq__(self, o: Self) -> bool:
        return self._equalize() == o._equalize()

    def _freeze(self):
        result = []
        for floor, items in self._equalize().items():
            result.append((floor, frozenset(items)))
        return frozenset(result)

    def __hash__(self) -> int:
        if self.hashed is None:
            self.hashed = hash(self._freeze())
        return self.hashed

    def __lt__(self, o: Self) -> bool:
        return len(self.get(3)) < len(o.get(3))


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
    start_state = get_start_state(additional_items)
    end_state = get_end_state(start_state)
    return search.bfs((0, start_state), (3, end_state), get_adjacent)


def get_start_state(additional_items: list[str]) -> State:
    state = State()
    for i, line in enumerate(Parser().lines()):
        # Remove period, pull the component string and split them
        components = line[:-1].split(" contains ")[1].split(", ")
        if i == 0:
            components += additional_items
        for component in components:
            # Example: and a plutonium-compatible microchip
            component_parts = component.split()
            raw_element, raw_item_type = component_parts[-2], component_parts[-1]
            element = raw_element.split("-")[0]
            if raw_item_type == "microchip":
                item_type = ItemType.CHIP
            elif raw_item_type == "generator":
                item_type = ItemType.GENERATOR
            else:
                item_type = None
            if item_type is not None:
                item = Item(element, item_type)
                state.add(i, item)
    return state


def get_end_state(start: State) -> State:
    state = State()
    for items in start.state.values():
        for item in items:
            state.add(3, item)
    return state


def get_adjacent(item: tuple[int, State]) -> list[tuple[int, State]]:
    level, state = item
    options = pair(state.get(level))

    adjacent = []
    for legal_state in get_legal(level, state, options, False):
        adjacent.append((level - 1, legal_state))
    for legal_state in get_legal(level, state, options, True):
        adjacent.append((level + 1, legal_state))
    return adjacent


def pair(items: set[Item]) -> list[list[Item]]:
    result = []

    # Any singular item
    for item in items:
        result.append([item])

    # Any pair of microcips
    chips = [item for item in items if item.item_type == ItemType.CHIP]
    for pair in itertools.combinations(chips, 2):
        result.append(list(pair))

    # Any pair of generators
    generators = [item for item in items if item.item_type == ItemType.GENERATOR]
    for pair in itertools.combinations(generators, 2):
        result.append(list(pair))

    # Some pair of matching chip and generator, all are equivalent
    matching_pair = get_matching_pair(chips, generators)
    if matching_pair is not None:
        result.append(matching_pair)

    return result


def get_matching_pair(
    chips: list[Item], generators: list[Item]
) -> Optional[list[Item]]:
    for chip in chips:
        for generator in generators:
            if chip.element == generator.element:
                return [chip, generator]
    return None


def get_legal(
    start_level: int, state: State, options: list[list[Item]], up: bool
) -> set[State]:
    legal = set()

    new_level = start_level + 1 if up else start_level - 1
    if new_level < 0 or new_level > 3:
        return legal

    # If we are going down but there is nothing below there is no point in moving things down
    if not up and state.total_below(start_level) == 0:
        return legal

    carry_1_options = [option for option in options if len(option) == 1]
    carry_2_options = [option for option in options if len(option) == 2]

    if up:
        # If we're going upstairs and can carry 2 things don't bother carrying one
        options = carry_2_options if len(carry_2_options) > 0 else carry_1_options
    else:
        # If we're going downstairs and can carry 1 thing don't bother carrying two
        options = carry_1_options if len(carry_1_options) > 0 else carry_2_options

    for option in options:
        new_state = state.move(new_level, option)
        if new_state.is_legal([start_level, new_level]):
            legal.add(new_state)

    return legal


if __name__ == "__main__":
    main()
