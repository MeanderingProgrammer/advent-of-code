from aoc import answer
from aoc.parser import Parser


def main() -> None:
    values = Parser().entries()
    index = get_index(int(values[-3][:-1]), int(values[-1][:-1]))
    answer.part1(19980801, get_password(index))


def get_index(row: int, column: int) -> int:
    row_start = 1
    for i in range(1, row):
        row_start += i
    index = row_start
    for i in range(row + 1, row + column):
        index += i
    return index


def get_password(n: int) -> int:
    password = 20_151_125
    for _ in range(1, n):
        password *= 252_533
        password %= 33_554_393
    return password


if __name__ == "__main__":
    main()
