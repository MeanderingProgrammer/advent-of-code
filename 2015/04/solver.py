import hashlib

from aoc import answer


def main() -> None:
    five_leading_0s = first_index(5, 1)
    answer.part1(346386, five_leading_0s)
    answer.part2(9958218, first_index(6, five_leading_0s))


def first_index(leading_zeros: int, index: int) -> int:
    goal = "0" * leading_zeros
    while True:
        value = "iwrupvqb" + str(index)
        hashed = hash(value)
        if hashed[:leading_zeros] == goal:
            return index
        index += 1


def hash(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest()


if __name__ == "__main__":
    main()
