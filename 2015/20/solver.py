import math
import itertools
from collections import defaultdict

import aoc_search
import aoc_util
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


GOAL = 29_000_000


def main():
    # Part 1 = 665280
    print(find_first(False))
    # Part 2 = 705600
    print(find_first(True))


def find_first(lazy):
    max_value = GOAL // 10
    houses = [0] * max_value
    for i in range(1, max_value):
        elve_end = min((i * 50) + 1, max_value) if lazy else max_value
        multiplier = 11 if lazy else 10
        for house in range(i, elve_end, i):
            houses[house] += (i * multiplier)
    return first(houses)


def first(houses):
    for i, house in enumerate(houses):
        if house >= GOAL:
            return i


if __name__ == '__main__':
    main()

