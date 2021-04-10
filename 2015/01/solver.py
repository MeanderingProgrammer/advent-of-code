from commons.aoc_parser import Parser


def main():
    data = Parser().string()
    # Part 1: 232
    print('Part 1: {}'.format(get_floor(data, False)))
    # Part 2: 1783
    print('Part 2: {}'.format(get_floor(data, True)))


def get_floor(value, stop_at_basement):
    floor = 0
    for i, ch in enumerate(value):
        if ch == '(':
            floor += 1
        else:
            floor -= 1
        if stop_at_basement and floor < 0:
            return i + 1
    return floor


if __name__ == '__main__':
    main()
