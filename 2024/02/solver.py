from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Report:
    levels: list[int]

    def safe(self, tolerant: bool) -> bool:
        index = self.check(None)
        if index is None:
            return True
        if tolerant:
            for i in range(max(index - 1, 0), min(index + 2, len(self.levels))):
                if self.check(i) is None:
                    return True
        return False

    def check(self, i: int | None) -> int | None:
        levels = self.levels
        if i is not None:
            levels = levels.copy()
            levels.pop(i)
        increase = levels[0] < levels[1]
        for i in range(len(levels) - 1):
            l1, l2 = levels[i], levels[i + 1]
            diff = abs(l1 - l2)
            if increase != (l1 < l2) or diff < 1 or diff > 3:
                return i
        return None


@answer.timer
def main() -> None:
    lines = Parser().lines()
    reports = [parse_report(line) for line in lines]
    answer.part1(402, count_safe(reports, False))
    answer.part2(455, count_safe(reports, True))


def parse_report(line: str) -> Report:
    return Report([int(v) for v in line.split()])


def count_safe(reports: list[Report], tolerant: bool) -> int:
    return sum([report.safe(tolerant) for report in reports])


if __name__ == "__main__":
    main()
