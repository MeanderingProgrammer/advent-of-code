from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    values = Parser().entries()
    row, column = int(values[-3][:-1]), int(values[-1][:-1])
    index = get_index(row, column)
    answer.part1(19980801, get_password(index))


def get_index(row: int, column: int) -> int:
    index = 1
    for i in range(1, row):
        index += i
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
