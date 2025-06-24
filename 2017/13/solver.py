from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Scanner:
    layer: int
    layer_range: int
    roundtrip: int

    def caught(self, offset: int) -> bool:
        return (self.layer + offset) % self.roundtrip == 0

    def severity(self) -> int:
        return self.layer * self.layer_range


@answer.timer
def main() -> None:
    scanners = get_scanners()
    answer.part1(632, trip_severity(scanners))
    offset = 1
    while is_caught(scanners, offset):
        offset += 1
    answer.part2(3849742, offset)


def get_scanners() -> list[Scanner]:
    def parse_scanner(line: str) -> Scanner:
        parts = line.split(": ")
        layer_range = int(parts[1])
        return Scanner(
            layer=int(parts[0]),
            layer_range=layer_range,
            roundtrip=(layer_range - 1) * 2,
        )

    return [parse_scanner(line) for line in Parser().lines()]


def trip_severity(scanners: list[Scanner]) -> int:
    result = 0
    for scanner in scanners:
        if scanner.caught(0):
            result += scanner.severity()
    return result


def is_caught(scanners: list[Scanner], offset: int) -> bool:
    for scanner in scanners:
        if scanner.caught(offset):
            return True
    return False


if __name__ == "__main__":
    main()
