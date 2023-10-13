from aoc import answer
from aoc.parser import Parser

DEAL = "deal with increment "
CUT = "cut "
NEW_STACK = "deal into new stack"


class Processors:
    def __init__(self, raw_values):
        self.processors = [self.__create(raw_value) for raw_value in raw_values]

    def apply(self, deck):
        for processor in self.processors:
            processor(deck)

    @staticmethod
    def __create(raw_value):
        if raw_value.startswith(DEAL):
            argument = int(raw_value[len(DEAL) :])
            return lambda deck: deck.deal(argument)
        elif raw_value.startswith(CUT):
            argument = int(raw_value[len(CUT) :])
            return lambda deck: deck.cut(argument)
        elif raw_value == NEW_STACK:
            return lambda deck: deck.deal_into_new()
        else:
            raise Exception("Unknown processor = {}".format(raw_value))


class Deck:
    def __init__(self, n):
        # Start in factory order, 0 at start up to n - 1
        self.__n = n
        self.__a = 1
        self.__b = 0

    def deal_into_new(self):
        self.apply(-1, -1)

    def cut(self, n):
        self.apply(1, -n)

    def deal(self, n):
        self.apply(n, 0)

    def apply(self, la, lb):
        self.__a = la * self.__a
        self.__b = la * self.__b + lb

    def index_of(self, index, times):
        a = self.calc_a(times)
        b = self.calc_b(a)
        return (a * index + b) % self.__n

    def get(self, index, times):
        a = self.calc_a(times)
        b = self.calc_b(a)
        return ((index - b) * self.inv(a)) % self.__n

    def calc_a(self, times):
        return pow(self.__a, times, self.__n)

    def calc_b(self, a):
        return (self.__b * (a - 1) * self.inv(self.__a - 1)) % self.__n

    def inv(self, a):
        return pow(a, self.__n - 2, self.__n)

    def __str__(self):
        return str(self.cards)


def main():
    # I have no idea how this one works, I definitely took it off the Reddits
    answer.part1(4684, process_deck(10_007).index_of(2019, 1))
    answer.part2(
        452290953297, process_deck(119_315_717_514_047).get(2020, 101_741_582_076_661)
    )


def process_deck(n):
    deck = Deck(n)
    processors = get_processors()
    processors.apply(deck)
    return deck


def get_processors():
    return Processors(Parser().lines())


if __name__ == "__main__":
    main()
