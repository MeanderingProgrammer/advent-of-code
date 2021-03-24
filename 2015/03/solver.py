from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


DIRECTIONS = {
    '^': Point(0, 1),
    'v': Point(0, -1),
    '<': Point(-1, 0),
    '>': Point(1, 0)
}

def main():
    # Part 1 = 2081
    run(1)
    # Part 2 = 2341
    run(2)

def run(santas):
    locations = []
    for i in range(santas):
        locations.append(Point(0, 0))

    visited = [location for location in locations]

    for i, direction in enumerate(Parser(FILE_NAME).string()):
        santa_index = i % len(locations)
        locations[santa_index] += DIRECTIONS[direction]
        visited.append(locations[santa_index])

    print('Unique houses = {}'.format(len(set(visited))))


if __name__ == '__main__':
    main()

