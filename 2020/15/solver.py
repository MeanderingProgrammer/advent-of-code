from aoc import answer
from aoc.parser import Parser
from dataclasses import dataclass
from typing import Optional


@dataclass
class Stats:
    new: int
    old: Optional[int] = None

    def next(self) -> int:
        return 0 if self.old is None else self.new - self.old

    def said(self, turn: int) -> None:
        self.old = self.new
        self.new = turn


def main():
    answer.part1(240, run(2_020))
    answer.part2(505, run(30_000_000))


def run(n) -> int:
    numbers = {}
    starter_numbers = Parser().int_csv()
    for i, value in enumerate(starter_numbers):
        numbers[value] = Stats(i)

    number = starter_numbers[-1]
    for i in range(len(numbers), n):
        number = numbers[number].next()
        stats = numbers.get(number)
        if stats is None:
            numbers[number] = Stats(i)
        else:
            stats.said(i)
    return number


if __name__ == "__main__":
    main()
