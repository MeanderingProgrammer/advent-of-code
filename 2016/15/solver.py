from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Disk:
    id: int
    positions: int
    start: int

    def passes(self, time: int) -> bool:
        position = time + self.id + self.start
        return position % self.positions == 0


def main():
    answer.part1(121834, calculate_first_pass(False))
    answer.part2(3208099, calculate_first_pass(True))


def calculate_first_pass(add_disk: bool) -> int:
    disks = get_disks()
    if add_disk:
        disks.append(Disk(len(disks) + 1, 11, 0))
    time = 1
    while not passes_all(disks, time):
        time += 1
    return time


def get_disks() -> list[Disk]:
    def parse_disk(line: str) -> Disk:
        parts = line.split()
        return Disk(int(parts[1][1:]), int(parts[3]), int(parts[11][:-1]))

    return [parse_disk(line) for line in Parser().lines()]


def passes_all(disks: list[Disk], time: int) -> bool:
    for disk in disks:
        if not disk.passes(time):
            return False
    return True


if __name__ == "__main__":
    main()
