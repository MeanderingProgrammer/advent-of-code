from collections import deque

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    num_elves = Parser().integer()
    answer.part1(1834903, solve_by_pattern(num_elves, True))
    answer.part2(1420280, solve_by_pattern(num_elves, False))


def solve_by_pattern(num_elves: int, increment: bool) -> int:
    winning_elve = 1
    for i in range(1, num_elves + 1):
        winning_elve += 1
        if increment or winning_elve > i // 2:
            winning_elve += 1
        if winning_elve > i:
            winning_elve = 1
    return winning_elve


# This function is used to find the patterns implemented in solve_by_pattern.
# It is not needed after the patterns are found but leaving it here for reference.
def get_patterns() -> None:
    # Part 1 pattern:
    # Winning elve increases by 2 for each elve we add.
    # If the winning elve > the total number of elves we start the pattern over.
    run_for_pattern(location_v1)
    # Part 2 pattern:
    # Winning elve increases by 1 for each elve we add.
    # If the winning elve > half the total number of elves we increase by 2.
    run_for_pattern(location_v2)


def run_for_pattern(location):
    for i in range(1, 100):
        print(i, run_with_n(location, i))


def run_with_n(location, n):
    elves, elves_left = get_start_state(n)
    while elves_left > 1:
        del elves[location(elves_left)]
        elves_left -= 1
        elves.rotate(-1)
    return elves[0] + 1


def location_v1(_: int) -> int:
    return 1


def location_v2(elves_left: int) -> int:
    return elves_left // 2


def get_start_state(n):
    return deque(range(n)), n


if __name__ == "__main__":
    main()
