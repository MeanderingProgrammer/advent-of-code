from aoc_parser import Parser


def main():
    file_name = 'data'
    parser = Parser('{}.txt'.format(file_name))
    solve_part_1(parser)
    solve_part_2(parser)


def solve_part_1(parser):
    # Part 1 = 540
    print('Final Frequency = {}'.format(sum(parser.int_lines())))


def solve_part_2(parser):
    # Part 2 = 73056
    print('First repeated value = {}'.format(get_first_repeated(parser.int_lines())))


def get_first_repeated(values):
    seen = set()
    result, i = 0, 0
    while True:
        if result in seen:
            return result
        seen.add(result)
        value = values[i % len(values)]
        result += value
        i += 1


if __name__ == '__main__':
    main()
