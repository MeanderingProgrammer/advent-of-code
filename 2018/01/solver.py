import commons.answer as answer
from commons.aoc_parser import Parser


def main():
    frequencies = Parser().int_lines()
    answer.part1(540, sum(frequencies))
    answer.part2(73056, get_first_repeated(frequencies))


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
