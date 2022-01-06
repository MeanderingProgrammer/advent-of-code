from collections import deque

import commons.answer as answer


STEPS = 344


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
    answer.part1(996, run_lock_after(2_017, 2_017))
    answer.part2(1898341, run_lock_after(50_000_000, 0))


def run_lock_after(steps, after):
    lock = Lock(STEPS)
    for i in range(steps + 1):
        lock.insert(i)
    return lock.after(after)


if __name__ == '__main__':
    main()
