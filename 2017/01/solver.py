from aoc import answer
from aoc.parser import Parser


def main():
    data = Parser().string()
    answer.part1(1136, sum_list(data, 1))
    answer.part2(1092, sum_list(data, len(data) // 2))


def sum_list(data, increment):
    values = []
    for i, entry in enumerate(data):
        next_index = (i + increment) % len(data)
        current_value = int(entry)
        next_value = int(data[next_index])
        if current_value == next_value:
            values.append(current_value)
    return sum(values)


if __name__ == "__main__":
    main()
