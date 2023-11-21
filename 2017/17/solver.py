from collections import deque

from aoc import answer
from aoc.parser import Parser


class Lock:
    def __init__(self, steps: int):
        self.q = deque()
        self.steps = steps

    def insert(self, value: int) -> None:
        self.q.rotate(-(self.steps + 1))
        self.q.appendleft(value)

    def after(self, value: int) -> int:
        index = self.q.index(value)
        return self.q[index + 1]


def main() -> None:
    answer.part1(996, run_lock_after(2_017, 2_017))
    answer.part2(1898341, run_lock_after(50_000_000, 0))


def run_lock_after(steps: int, after: int) -> int:
    lock = Lock(Parser().integer())
    for i in range(steps + 1):
        lock.insert(i)
    return lock.after(after)


if __name__ == "__main__":
    main()
