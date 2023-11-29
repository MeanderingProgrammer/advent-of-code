import itertools

from aoc import answer
from aoc.parser import Parser


def main() -> None:
    combinations = get_combinations(Parser().int_lines(), 150)
    answer.part1(1304, len(combinations))
    answer.part2(18, num_min(combinations))


def get_combinations(capacities: list[int], volume: int) -> list[tuple[int, ...]]:
    combinations = []
    for i in range(2, len(capacities)):
        for combination in itertools.combinations(capacities, i):
            if sum(combination) == volume:
                combinations.append(combination)
    return combinations


def num_min(combinations: list[tuple[int, ...]]) -> int:
    lengths: list[int] = [len(combination) for combination in combinations]
    return sum([length == min(lengths) for length in lengths])


if __name__ == "__main__":
    main()
