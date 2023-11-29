from aoc import answer
from aoc.parser import Parser


def main() -> None:
    data = Parser().string()
    answer.part1(1136, sum_list(data, 1))
    answer.part2(1092, sum_list(data, len(data) // 2))


def sum_list(data: str, increment: int) -> int:
    values: list[int] = []
    for i, entry in enumerate(data):
        next_index = (i + increment) % len(data)
        if entry == data[next_index]:
            values.append(int(entry))
    return sum(values)


if __name__ == "__main__":
    main()
