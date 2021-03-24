import math
import itertools
from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'
TOTAL_VOLUME = 25 if TEST else 150


def main():
    capacities = get_capacities()
    combinations = get_combinations(capacities)
    # Part 1 = 1304
    print(len(combinations))
    # Part 2 = 18
    print(get_min_lengths(combinations))


def get_combinations(capacities):
    combinations = []
    for i in range(2, len(capacities)):
        for combination in itertools.combinations(capacities, i):
            if sum(combination) == TOTAL_VOLUME:
                combinations.append(combination)
    return combinations


def get_min_lengths(combinations):
    lengths = [len(combination) for combination in combinations]
    min_length = min(lengths)
    return sum([length == min_length for length in lengths])


def get_capacities():
    return Parser(FILE_NAME).int_lines()


if __name__ == '__main__':
    main()

