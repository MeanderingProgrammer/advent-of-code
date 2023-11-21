import hashlib

from aoc import answer
from aoc.parser import Parser


def main() -> None:
    prefix = Parser(strip=True).string()
    five_leading_0s = first_index(prefix, 5, 1)
    answer.part1(346386, five_leading_0s)
    answer.part2(9958218, first_index(prefix, 6, five_leading_0s))


def first_index(prefix: str, leading_zeros: int, index: int) -> int:
    goal = "0" * leading_zeros
    while True:
        value = prefix + str(index)
        hashed = hashlib.md5(value.encode()).hexdigest()
        if hashed[:leading_zeros] == goal:
            return index
        index += 1


if __name__ == "__main__":
    main()
