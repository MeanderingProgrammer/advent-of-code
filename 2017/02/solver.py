from typing import Callable

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    answer.part1(47623, calculate_checksum(checksum_v1))
    answer.part2(312, calculate_checksum(checksum_v2))


def calculate_checksum(f: Callable[[list[int]], int]) -> int:
    result = 0
    for line in Parser().lines():
        values = [int(value) for value in line.split()]
        result += f(values)
    return result


def checksum_v1(values: list[int]) -> int:
    return max(values) - min(values)


def checksum_v2(values: list[int]) -> int:
    for i, v1 in enumerate(values[:-1]):
        for v2 in values[i + 1 :]:
            num, denom = max(v1, v2), min(v1, v2)
            if num % denom == 0:
                return num // denom
    raise Exception("Failed")


if __name__ == "__main__":
    main()
