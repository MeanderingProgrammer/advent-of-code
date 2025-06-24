from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    values = Parser().int_lines()
    answer.part1(1020084, find_pair(values, 2020, set()))
    answer.part2(295086480, find_triple(values, 2020))


def find_pair(values: list[int], goal: int, ignore: set[int]) -> int | None:
    for value in values:
        if value not in ignore:
            needed = goal - value
            if needed in values:
                return value * needed
    return None


def find_triple(values: list[int], goal: int) -> int:
    ignore: set[int] = set()
    for value in values:
        ignore.add(value)
        pair = find_pair(values, goal - value, ignore)
        if pair is not None:
            return value * pair
    raise Exception("Failed")


if __name__ == "__main__":
    main()
