import hashlib
from typing import Callable

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    prefix = Parser().string()
    answer.part1("d4cd2ee1", get_password(prefix, part1))
    answer.part2("f2c730e5", get_password(prefix, part2))


def get_password(prefix: str, update: Callable[[list[str], str], None]) -> str:
    password, i = [""] * 8, 0
    while not all(password):
        value = prefix + str(i)
        digest = hashlib.md5(str.encode(value)).hexdigest()
        if digest[:5] == "00000":
            update(password, digest)
        i += 1
    return "".join(password)


def part1(password: list[str], digest: str) -> None:
    index = sum([ch != "" for ch in password])
    password[index] = digest[5]


def part2(password: list[str], digest: str) -> None:
    index = digest[5]
    valid_indexes = [str(i) for i in range(len(password))]
    if index in valid_indexes:
        index = int(index)
        if password[index] == "":
            password[index] = digest[6]


if __name__ == "__main__":
    main()
