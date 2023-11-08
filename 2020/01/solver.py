from aoc import answer
from aoc.parser import Parser


def main():
    values = read_data()

    pair = find_pair(2020, values)
    answer.part1(1020084, pair[0] * pair[1])

    triple = find_triple(values)
    answer.part2(295086480, triple[0] * triple[1] * triple[2])


def find_triple(values):
    ignore = set()
    for value in values:
        needed = 2020 - value
        ignore.add(value)
        # Remove value from values
        pair = find_pair(needed, values, ignore)
        if pair is not None:
            return (value, pair[0], pair[1])


def find_pair(goal, values, ignore=None):
    for value in values:
        if ignore is None or value not in ignore:
            needed = goal - value
            if needed in values:
                return (value, needed)
    return None


def read_data():
    return Parser().int_lines()


if __name__ == "__main__":
    main()
