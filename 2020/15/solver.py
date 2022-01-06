import commons.answer as answer
from commons.aoc_parser import Parser


class Stats:

    def __init__(self, turn):
        self.turns = [turn]

    def is_new(self):
        return len(self.turns) == 1

    def said(self, turn):
        self.turns.append(turn)
        if len(self.turns) > 2:
            self.turns = self.turns[1:]

    def get_difference(self):
        return self.turns[-1] - self.turns[-2]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.turns)


def main():
    answer.part1(240, run(2_020))
    answer.part2(505, run(30_000_000))


def run(n):
    numbers = {}
    for i, value in enumerate(process()):
        stats = Stats(i)
        numbers[value] = stats
        previous = (value, stats)

    for i in range(len(numbers), n):
        to_say = 0 if previous[1].is_new() else previous[1].get_difference()
        next_stats = numbers[to_say] if to_say in numbers else None

        if next_stats is None:
            next_stats = Stats(i)
            numbers[to_say] = next_stats
        else:
            next_stats.said(i)
        previous = (to_say, next_stats)

    return previous[0]


def process():
    return Parser().int_csv()


if __name__ == '__main__':
    main()
