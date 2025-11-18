from collections import deque

from aoc import answer
from aoc.parser import Parser


class Lock:
    def __init__(self, steps: int):
        self.q: deque[int] = deque()
        self.steps: int = steps

    def insert(self, value: int) -> None:
        self.q.rotate(-(self.steps + 1))
        self.q.appendleft(value)

    def after(self, value: int) -> int:
        index = self.q.index(value)
        return self.q[index + 1]


@answer.timer
def main() -> None:
    steps = Parser().integer()
    answer.part1(996, run_lock_after(steps, 2_017, 2_017))
    answer.part2(1898341, run_lock_after(steps, 50_000_000, 0))


def run_lock_after(steps: int, rounds: int, after: int) -> int:
    lock = Lock(steps)
    for i in range(rounds + 1):
        lock.insert(i)
    return lock.after(after)


if __name__ == "__main__":
    main()
