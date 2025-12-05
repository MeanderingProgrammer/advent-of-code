from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    values = Parser().int_lines()
    answer.part1(1292, increases(values, 1))
    answer.part2(1262, increases(values, 3))


def increases(values: list[int], n: int) -> int:
    result = 0
    for i in range(len(values) - n):
        if sum(values[i + 1 : i + 1 + n]) > sum(values[i : i + n]):
            result += 1
    return result


if __name__ == "__main__":
    main()
