from aoc_parser import Parser


def main():
    file_name = 'data'
    frequencies = Parser('{}.txt'.format(file_name)).int_lines()
    # Part 1: 540
    print('Part 1: {}'.format(sum(frequencies)))
    # Part 2: 73056
    print('Part 2: {}'.format(get_first_repeated(frequencies)))


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
