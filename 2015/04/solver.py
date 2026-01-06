import hashlib

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    prefix = Parser().string()
    five_leading = first_index(prefix, 5, 1)
    answer.part1(346386, five_leading)
    answer.part2(9958218, first_index(prefix, 6, five_leading))


def first_index(prefix: str, zeros: int, index: int) -> int:
    goal = "0" * zeros
    while True:
        value = prefix + str(index)
        hashed = hashlib.md5(value.encode()).hexdigest()
        if hashed[:zeros] == goal:
            return index
        index += 1


if __name__ == "__main__":
    main()
