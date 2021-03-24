from aoc_parser import Parser
from aoc_board import Grid, Point


FILE_NAME = 'data'


def main():
    data = Parser(FILE_NAME).read()
    # Part 1 = 1136
    sum_list(data, 1)
    # Part 2 = 1092
    sum_list(data, len(data) // 2)


def sum_list(data, increment):
    values = []
    for i, entry in enumerate(data):
        next_index = (i + increment) % len(data)
        current_value = int(entry)
        next_value = int(data[next_index])
        if current_value == next_value:
            values.append(current_value)
    print('Sum = {}'.format(sum(values)))


if __name__ == '__main__':
    main()

