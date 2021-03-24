import math
import itertools
from collections import defaultdict

import aoc_search
import aoc_util
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
POSITION = (4, 3) if TEST else (2_947, 3_029)


def main():
    index = get_index(POSITION)
    # Part 1 = 19980801
    print(get_password(index))


def get_index(position):
    row, column = position
    row_start = 1
    for i in range(1, row):
        row_start += i
    index = row_start
    for i in range(row + 1, row + column):
        index += i
    return index


def get_password(n):
    password = 20_151_125
    for i in range(1, n):
        password *= 252_533
        password %= 33_554_393
    return password


if __name__ == '__main__':
    main()

