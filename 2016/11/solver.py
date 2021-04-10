import itertools

import commons.aoc_search as aoc_search
from commons.aoc_parser import Parser


class State:

    def __init__(self):
        # 4 floors with nothing on at first
        self.state = {i: set() for i in range(4)}
        self.hashed = None

    def add(self, floor, item, parse=False):
        if parse:
            item = item.split()
            value, item_type = item[-2], item[-1]
            if item_type == 'generator':
                item = Generator(value)
            elif item_type == 'microchip':
                item = Chip(value)
            else:
                item = None
        if item is not None:
            self.state[floor].add(item)

    def get(self, floor):
        return self.state[floor]

    def total_below(self, floor):
        return sum([
            len(self.state[level]) for level in range(floor)
        ])

    def move(self, items_to_move, new_level):
        new_state = State()
        for floor, items in self.state.items():
            for item in items:
                if item not in items_to_move:
                    new_state.add(floor, item)
        for item_to_move in items_to_move:
            new_state.add(new_level, item_to_move)
        return new_state

    def is_legal(self, floors):
        for floor in floors:
            if self.contains_unpaired_chip(floor):
                return False
        return True

    def contains_unpaired_chip(self, floor):
        items = self.get(floor)
        chips = [item for item in items if isinstance(item, Chip)]
        generators = [item for item in items if isinstance(item, Generator)]

        if len(chips) == 0 or len(generators) == 0:
            return False

        for chip in chips:
            if chip.generator() not in generators:
                return True

        return False

    def _freeze(self):
        result = set()
        for floor, items in self.state.items():
            result.add((floor, frozenset(items)))
        return frozenset(result)

    def __eq__(self, o):
        return self.state == o.state

    def __hash__(self):
        if self.hashed is None:
            self.hashed = hash(self._freeze())
        return self.hashed

    def __lt__(self, o):
        return len(self.get(3)) < len(o.get(3))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.state)


class Generator:

    def __init__(self, value):
        self.value = value.upper()

    def __eq__(self, o):
        return self.value == o.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value[0]


class Chip:

    def __init__(self, value):
        self.value = value.split('-')[0].lower()

    def generator(self):
        return Generator(self.value)

    def __eq__(self, o):
        return self.value == o.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value[0]


def main():
    # Part 1: 37
    print('Part 1: {}'.format(count_steps([])))
    # Part 2: 61 
    print('Part 2: {}'.format(count_steps([
        'elerium generator',
        'elerium-compatible microchip',
        'dilithium generator',
        'dilithium-compatible microchip'
    ])))


def count_steps(add_to_first):
    start_state = get_start_state(add_to_first)
    end_state = get_end_state(start_state)

    return aoc_search.bfs(
        (0, start_state),
        (3, end_state),
        get_adjacent
    )


def get_start_state(additonal):
    state = State()
    for i, line in enumerate(Parser().lines()):
        components = line[:-1].split(' contains ')[1].split(', ')
        if i == 0:
            components += additonal
        for component in components:
            state.add(i, component, True)
    return state


def get_end_state(start):
    state = State()
    for items in start.state.values():
        for item in items:
            state.add(3, item)
    return state


def get_adjacent(item):
    level, state = item

    options = pair(state.get(level))

    adjacent = set()

    for legal_state in get_legal(level, state, options, False):
        adjacent.add((level - 1, legal_state))

    for legal_state in get_legal(level, state, options, True):
        adjacent.add((level + 1, legal_state)) 

    return adjacent


def pair(items):
    result = []

    # Any singular item
    for item in items:
        result.append([item])

    chips = [item for item in items if isinstance(item, Chip)]
    generators = [item for item in items if isinstance(item, Generator)]

    # Any pair of microcips
    for pair in itertools.combinations(chips, 2):
        result.append(list(pair))

    # Any pair of generators
    for pair in itertools.combinations(generators, 2):
        result.append(list(pair))

    # Some pair of matching chip and generator, all are equivalent
    matching_pair = get_matching_pair(chips, generators)
    if matching_pair is not None:
        result.append(matching_pair)

    return result


def get_matching_pair(chips, generators):
    for chip in chips:
        generator = chip.generator()
        if generator in generators:
            return [chip, generator]
    return None


def get_legal(start_level, state, options, up):
    legal = set()

    new_level = start_level + 1 if up else start_level - 1
    if new_level < 0 or new_level > 3:
        return legal

    # If we are going down but there is nothing below
    # then there is no point in moving things down
    if not up and state.total_below(start_level) == 0:
        return legal

    on_level = state.get(new_level)

    carry_1_options = [option for option in options if len(option) == 1]
    carry_2_options = [option for option in options if len(option) == 2]

    if up:
        # If we're going upstairs and can carry 2 things don't bother carrying one
        options = carry_2_options if len(carry_2_options) > 0 else carry_1_options
    else:
        # If we're going downstairs and can carry 1 thing don't bother carrying two
        options = carry_1_options if len(carry_1_options) > 0 else carry_2_options

    for option in options:
        new_state = state.move(option, new_level)
        if new_state.is_legal([start_level, new_level]):
            legal.add(new_state)

    return legal


if __name__ == '__main__':
    main()
