import itertools

from aoc_parser import Parser


FILE_NAME = 'data'
TOTAL_VOLUME = 150


def main():
    capacities = get_capacities()
    combinations = get_combinations(capacities)
    # Part 1: 1304
    print('Part 1: {}'.format(len(combinations)))
    # Part 2: 18
    print('Part 2: {}'.format(get_min_lengths(combinations)))


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
