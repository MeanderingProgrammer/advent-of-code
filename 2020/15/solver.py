from dataclasses import dataclass
from typing import Optional

from aoc import answer
from aoc.parser import Parser


@dataclass
class Stats:
    new: int
    old: Optional[int] = None

    def next(self) -> int:
        return 0 if self.old is None else self.new - self.old

    def said(self, turn: int) -> None:
        self.old = self.new
        self.new = turn


@answer.timer
def main() -> None:
    values = Parser().int_csv()
    answer.part1(240, run(values, 2_020))
    answer.part2(505, run(values, 30_000_000))


def run(values: list[int], n: int) -> int:
    number_stats: list[Optional[Stats]] = [None] * n
    for i, value in enumerate(values):
        number_stats[value] = Stats(i)
    number = values[-1]
    for i in range(len(values), n):
        current_stats = number_stats[number]
        assert current_stats is not None
        number = current_stats.next()
        stats = number_stats[number]
        if stats is not None:
            stats.said(i)
        else:
            number_stats[number] = Stats(i)
    return number


if __name__ == "__main__":
    main()
