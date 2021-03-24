import itertools
from collections import defaultdict


import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'

GENERATOR = 'generator'
MICRO_CHIP = 'microchip'


class Generator:

    def __init__(self, value):
        self.value = value

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}G'.format(self.value[0].upper())


class Chip:

    def __init__(self, value):
        self.value = value.split('-')[0]

    def generator(self):
        return Generator(self.value)

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}M'.format(self.value[0].upper())


def main():
    # Part 1 = 37
    count_steps([])
    # Part 2 = 61 
    count_steps([
        'elerium generator',
        'elerium-compatible microchip',
        'dilithium generator',
        'dilithium-compatible microchip'
    ])


def count_steps(add_to_first):
    start_state = get_start_state(add_to_first)
    end_state = get_end_state(start_state)

    result = aoc_search.bfs(
        (0, freeze(start_state)), 
        (3, freeze(end_state)), 
        get_adjacent
    )
    print('Steps taken = {}'.format(result))


def get_adjacent(item):
    level = item[0]
    state = unfreeze(item[1])

    options = pair(state[level])

    adjacent = set()
    for legal_state in get_legal(state, options, level, False):
        adjacent.add((level - 1, legal_state))
    for legal_state in get_legal(state, options, level, True):
        adjacent.add((level + 1, legal_state)) 

    return adjacent


def get_legal(state, options, start_level, up):
    legal = set()

    new_level = start_level + 1 if up else start_level - 1
    if new_level < 0 or new_level > 3:
        return legal

    # If we are going down but there is nothing below
    # then there is no point in moving things down
    if not up:
        total_below = sum([
            len(state[level]) for level in range(new_level + 1)
        ])
        if total_below == 0:
            return legal

    on_level = state[new_level]

    carry_2_options = [option for option in options if type(option) is tuple]
    carry_1_options = [option for option in options if type(option) is not tuple]

    if up:
        # If we're going upstairs and can carry 2 things don't bother carrying one
        options = carry_2_options if len(carry_2_options) > 0 else carry_1_options
    else:
        # If we're going downstairs and can carry 1 thing don't bother carrying two
        options = carry_1_options if len(carry_1_options) > 0 else carry_2_options

    for option in options:
        if type(option) is tuple:
            option = [option[0], option[1]]
        else:
            option = [option] 
        if is_legal(option, on_level):
            for o in option:
                move(state, start_level, new_level, o)
            legal.add(freeze(state))
            for o in option:
                move(state, new_level, start_level, o)

    return legal


def move(state, start_level, new_level, value):
    state[start_level].remove(value)
    state[new_level].add(value)


def is_legal(option, on_level):
    if len(option) == 1:
        return check_legality(option[0], on_level)
    else:
        on_level.add(option[0])
        first_legal = check_legality(option[1], on_level)
        on_level.remove(option[0])

        on_level.add(option[1])
        second_legal = check_legality(option[0], on_level)
        on_level.remove(option[1])

        return first_legal and second_legal


def check_legality(item, on_level):
    generators = [g for g in on_level if isinstance(g, Generator)]
    if isinstance(item, Chip):
        return len(generators) == 0 or item.generator() in generators
    else:
        generators += [item]
        chips_powered = [c.generator() in generators for c in on_level if isinstance(c, Chip)]
        return all(chips_powered)


def pair(items):
    result = set()

    # Any singular item
    for item in items:
        result.add(item)

    # Any pair of microcips
    chips = [item for item in items if isinstance(item, Chip)]
    for pair in itertools.combinations(chips, 2):
        result.add(pair)

    # Any pair of generators
    generators = [item for item in items if isinstance(item, Generator)]
    for pair in itertools.combinations(generators, 2):
        result.add(pair)

    # Some pair of matching chip and generator, all are equivalent
    for chip in chips:
        generator = chip.generator()
        if generator in items:
            result.add((chip, generator))
            break

    return result


def unfreeze(state):
    result = {}
    for value in state:
        result[value[0]] = set(value[1])
    return result


def freeze(value):
    result = set()
    for item in value.items():
        result.add((item[0], frozenset(item[1])))
    return frozenset(result)


def get_start_state(add_to_first):
    floors = get_base()
    for i, line in enumerate(Parser(FILE_NAME).lines()):
        components = line[:-1].split(',')
        if i == 0:
            components += add_to_first
        for elements in components:
            elements = elements.split()
            value, component = elements[-2], elements[-1]
            if component == GENERATOR:
                floors[i].add(Generator(value))
            elif component == MICRO_CHIP:
                floors[i].add(Chip(value))
    return floors


def get_end_state(start_state):
    end_state = get_base()
    for floor, items in start_state.items():
        for item in items:
            end_state[3].add(item)
    return end_state


def get_base():
    return {
        0: set(),
        1: set(),
        2: set(),
        3: set()
    }


def print_state(state):
    print(0, state[0])
    print(1, state[1])
    print(2, state[2])
    print(3, state[3])


if __name__ == '__main__':
    main()

