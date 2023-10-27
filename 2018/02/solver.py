from collections import defaultdict

from aoc import answer
from aoc.parser import Parser


def main():
    box_ids = Parser().lines()
    contain_2 = count_contain_exactly(box_ids, 2)
    contain_3 = count_contain_exactly(box_ids, 3)
    answer.part1(5434, contain_2 * contain_3)
    answer.part2("agimdjvlhedpsyoqfzuknpjwt", get_most_overlap(box_ids))


def count_contain_exactly(values, n):
    return sum([contains_exactly(value, n) for value in values])


def contains_exactly(value, n):
    frequencies = defaultdict(int)
    for character in value:
        frequencies[character] += 1
    return n in frequencies.values()


def get_most_overlap(box_ids):
    for i, box_1 in enumerate(box_ids):
        for box_2 in box_ids[i + 1 :]:
            overlap = get_overlap(box_1, box_2)
            if len(overlap) == len(box_1) - 1:
                return overlap


def get_overlap(value_1, value_2):
    overlap = []
    for v1, v2 in zip(value_1, value_2):
        if v1 == v2:
            overlap.append(v1)
    return "".join(overlap)


if __name__ == "__main__":
    main()
