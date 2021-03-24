from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
GEN_A_START = 65 if TEST else 277
GEN_B_START = 8_921 if TEST else 349


class Generator:

    def __init__(self, value, factor, mult):
        self.value = value
        self.factor = factor
        self.mult = mult

    def next(self, wait_for_mult):
        self.calculate()
        if wait_for_mult:
            while self.value % self.mult != 0:
                self.calculate()
        return self.value

    def calculate(self):
        self.value *= self.factor
        self.value %= 2_147_483_647


class Judge:

    def equal(self, v1, v2):
        v1 = bin(v1)[-16:]
        v2 = bin(v2)[-16:]
        return v1 == v2


def main():
    judge = Judge()
    # Part 1 = 592
    count_matches(judge, 40_000_000, False)
    # Part 2 = 320
    count_matches(judge, 5_000_000, True)


def count_matches(judge, n, wait_for_mult):
    count = 0

    gen_a = Generator(GEN_A_START, 16_807, 4)
    gen_b = Generator(GEN_B_START, 48_271, 8)

    for i in range(n):
        if i % 100_000 == 0:
            print(i)
        if judge.equal(gen_a.next(wait_for_mult), gen_b.next(wait_for_mult)):
            count += 1
    print('Total matches = {}'.format(count))


if __name__ == '__main__':
    main()

