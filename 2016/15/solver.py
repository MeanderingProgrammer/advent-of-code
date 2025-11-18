from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Disk:
    id: int
    positions: int
    start: int

    @classmethod
    def new(cls, s: str) -> Self:
        parts = s.split()
        return cls(int(parts[1][1:]), int(parts[3]), int(parts[11][:-1]))

    def passes(self, time: int) -> bool:
        position = time + self.id + self.start
        return position % self.positions == 0


@answer.timer
def main() -> None:
    disks = [Disk.new(line) for line in Parser().lines()]

    part1 = calculate_first_pass(disks)
    disks.append(Disk(len(disks) + 1, 11, 0))
    part2 = calculate_first_pass(disks)

    answer.part1(121834, part1)
    answer.part2(3208099, part2)


def calculate_first_pass(disks: list[Disk]) -> int:
    time = 1
    while not passes_all(disks, time):
        time += 1
    return time


def passes_all(disks: list[Disk], time: int) -> bool:
    for disk in disks:
        if not disk.passes(time):
            return False
    return True


if __name__ == "__main__":
    main()
