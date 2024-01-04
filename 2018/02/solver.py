from collections import defaultdict

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    box_ids = Parser().lines()
    contain_2 = count_contain_exactly(box_ids, 2)
    contain_3 = count_contain_exactly(box_ids, 3)
    answer.part1(5434, contain_2 * contain_3)
    answer.part2("agimdjvlhedpsyoqfzuknpjwt", get_most_overlap(box_ids))


def count_contain_exactly(values: list[str], n: int) -> int:
    return sum([contains_exactly(value, n) for value in values])


def contains_exactly(value: str, n: int) -> bool:
    frequencies = defaultdict(int)
    for character in value:
        frequencies[character] += 1
    return n in frequencies.values()


def get_most_overlap(box_ids: list[str]) -> str:
    for i, box_1 in enumerate(box_ids):
        for box_2 in box_ids[i + 1 :]:
            overlap = get_overlap(box_1, box_2)
            if len(overlap) == len(box_1) - 1:
                return overlap
    raise Exception("Failed")


def get_overlap(value_1: str, value_2: str) -> str:
    overlap: str = ""
    for v1, v2 in zip(value_1, value_2):
        if v1 == v2:
            overlap += v1
    return overlap


if __name__ == "__main__":
    main()
