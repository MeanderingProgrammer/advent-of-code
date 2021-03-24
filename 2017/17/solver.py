from collections import deque

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
STEPS = 3 if TEST else 344


class Lock:

    def __init__(self, steps):
        self.q = deque()
        self.steps = steps

    def insert(self, value):
        self.q.rotate(-(self.steps + 1))
        self.q.appendleft(value)

    def after(self, value):
        index = self.q.index(value)
        return self.q[index + 1]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.q)


def main():
    # Part 1 = 996
    lock = run_lock(2_017)
    print('Value after 2017 = {}'.format(lock.after(2_017)))
    # Part 2 = 1898341
    lock = run_lock(50_000_000)
    print('Value after 0 = {}'.format(lock.after(0)))


def run_lock(steps):
    lock = Lock(STEPS)
    for i in range(steps + 1):
        if i % 1_000_000 == 0:
            print(i)
        lock.insert(i)
    return lock


if __name__ == '__main__':
    main()

