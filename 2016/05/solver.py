import hashlib
from typing import Callable

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    door_id = Parser().string()
    answer.part1("d4cd2ee1", generate_password(door_id, populate_v1))
    answer.part2("f2c730e5", generate_password(door_id, populate_v2))


def generate_password(door_id: str, populator: Callable[[list[str], str], None]) -> str:
    password, i = [""] * 8, 0
    while not all(password):
        value = door_id + str(i)
        hashed = hashlib.md5(str.encode(value)).hexdigest()
        if hashed[:5] == "00000":
            populator(password, hashed)
        i += 1
    return "".join(password)


def populate_v1(password: list[str], hashed: str) -> None:
    index = sum([ch != "" for ch in password])
    password[index] = hashed[5]


def populate_v2(password: list[str], hashed: str) -> None:
    index = hashed[5]
    valid_indexes = [str(i) for i in range(len(password))]
    if index in valid_indexes:
        index = int(index)
        if password[index] == "":
            password[index] = hashed[6]


if __name__ == "__main__":
    main()
