import itertools

from aoc import answer
from aoc.parser import Parser


def main():
    capacities = get_capacities()
    volume = 150
    combinations = get_combinations(capacities, volume)
    answer.part1(1304, len(combinations))
    answer.part2(18, get_min_lengths(combinations))


def get_combinations(capacities, volume):
    combinations = []
    for i in range(2, len(capacities)):
        for combination in itertools.combinations(capacities, i):
            if sum(combination) == volume:
                combinations.append(combination)
    return combinations


def get_min_lengths(combinations):
    lengths = [len(combination) for combination in combinations]
    min_length = min(lengths)
    return sum([length == min_length for length in lengths])


def get_capacities():
    return Parser().int_lines()


if __name__ == "__main__":
    main()
