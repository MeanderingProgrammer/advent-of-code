from aoc import answer
from aoc.parser import Parser
from collections import defaultdict


def main():
    answer.part1("liwvqppc", error_correct_message(-1))
    answer.part2("caqfbzlh", error_correct_message(0))


def error_correct_message(n):
    words = get_words()
    frequencies = [defaultdict(int) for i in range(len(words[0]))]

    for word in words:
        for i, letter in enumerate(word):
            frequencies[i][letter] += 1

    message = [nth_most_common(frequency, n) for frequency in frequencies]
    return "".join(message)


def nth_most_common(frequency, n):
    items = [(item[1], item[0]) for item in frequency.items()]
    items.sort()
    return items[n][1]


def get_words():
    return Parser().lines()


if __name__ == "__main__":
    main()
