from aoc import answer
from aoc.parser import Parser


def main() -> None:
    frequencies = Parser().int_lines()
    answer.part1(540, sum(frequencies))
    answer.part2(73056, first_repeated(frequencies))


def first_repeated(values: list[int]) -> int:
    seen: set[int] = set()
    result: int = 0
    i: int = 0
    while True:
        if result in seen:
            return result
        seen.add(result)
        value = values[i % len(values)]
        result += value
        i += 1


if __name__ == "__main__":
    main()
