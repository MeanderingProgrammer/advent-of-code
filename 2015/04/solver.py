import hashlib
from aoc import answer

SALT = "iwrupvqb"


def main():
    five_leading_0s = first_index(5, 1)
    answer.part1(346386, five_leading_0s)
    answer.part2(9958218, first_index(6, five_leading_0s))


def first_index(leading_zeros, index):
    goal = "0" * leading_zeros
    while True:
        value = SALT + str(index)
        hashed = hash(value)
        if hashed[:leading_zeros] == goal:
            return index
        index += 1


def hash(value):
    return hashlib.md5(value.encode()).hexdigest()


if __name__ == "__main__":
    main()
