from collections import deque

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
NUM_ELVES = 5 if TEST else 3_014_603


def main():
    # Part 1 = 1834903
    run(location_v1)
    # Part 2 = 1420280
    run(location_v2)

'''
Really slow for part 2, like 2 hours to finish
'''
def run(location):
    elves, elves_left = get_start_state()

    while elves_left > 1:
        del elves[location(elves_left)]
        elves.rotate(-1)
        elves_left -= 1

    winner = elves[0] + 1
    print('Winner = {}'.format(winner))


def location_v1(elves_left):
    return 1


def location_v2(elves_left):
    return elves_left // 2


def get_start_state():
    return deque(range(NUM_ELVES)), NUM_ELVES


if __name__ == '__main__':
    main()

