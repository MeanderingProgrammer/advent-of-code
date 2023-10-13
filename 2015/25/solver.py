from aoc import answer


POSITION = (2_947, 3_029)


def main():
    index = get_index(POSITION)
    answer.part1(19980801, get_password(index))


def get_index(position):
    row, column = position
    row_start = 1
    for i in range(1, row):
        row_start += i
    index = row_start
    for i in range(row + 1, row + column):
        index += i
    return index


def get_password(n):
    password = 20_151_125
    for i in range(1, n):
        password *= 252_533
        password %= 33_554_393
    return password


if __name__ == "__main__":
    main()
