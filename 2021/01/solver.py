from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    values = Parser().int_lines()
    answer.part1(1292, window_increases(values, 1))
    answer.part2(1262, window_increases(values, 3))


def window_increases(values: list[int], window_size: int) -> int:
    increases = 0
    for i in range(len(values) - window_size):
        if sum(values[i + 1 : i + 1 + window_size]) > sum(values[i : i + window_size]):
            increases += 1
    return increases


if __name__ == "__main__":
    main()
