from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]


@dataclass(frozen=True)
class Part:
    number: int
    row: int
    start: int
    end: int

    def is_in(self, locations: set[Point]):
        return len(self.adjacent().intersection(locations)) > 0

    def adjacent(self) -> set[Point]:
        left: list[Point] = [
            (self.start - 1, self.row + 1),
            (self.start - 1, self.row),
            (self.start - 1, self.row - 1),
        ]
        right: list[Point] = [
            (self.end + 1, self.row + 1),
            (self.end + 1, self.row),
            (self.end + 1, self.row - 1),
        ]
        result: set[Point] = set(left + right)
        for x in range(self.start, self.end + 1):
            result.update([(x, self.row + 1), (x, self.row - 1)])
        return result


@dataclass(frozen=True)
class Symbol:
    location: Point
    value: str

    def ratio(self, parts: list[Part]) -> int:
        if self.value != "*":
            return 0
        adjacent = [part for part in parts if self.location in part.adjacent()]
        if len(adjacent) != 2:
            return 0
        p1, p2 = adjacent
        return p1.number * p2.number


@answer.timer
def main() -> None:
    lines: list[str] = Parser(strip=True).lines()
    parts: list[Part] = get_parts(lines)
    symbols: list[Symbol] = get_symbols(lines)
    locations = set([symbol.location for symbol in symbols])
    parts = [part for part in parts if part.is_in(locations)]
    answer.part1(539713, sum(part.number for part in parts))
    answer.part2(84159075, sum(gear.ratio(parts) for gear in symbols))


def get_parts(lines: list[str]) -> list[Part]:
    result: list[Part] = []
    for y, line in enumerate(lines):
        locations = get_digit_locations(line)
        for location in locations:
            number = int(line[location[0] : location[1] + 1])
            part = Part(number=number, row=y, start=location[0], end=location[1])
            result.append(part)
    return result


def get_digit_locations(line: str) -> list[tuple[int, int]]:
    digits = [i for i in range(len(line)) if line[i].isdigit()]
    result: list[tuple[int, int]] = []
    start = 0
    for i in range(1, len(digits)):
        if digits[i - 1] + 1 != digits[i]:
            result.append((digits[start], digits[i - 1]))
            start = i
    result.append((digits[start], digits[-1]))
    return result


def get_symbols(lines: list[str]) -> list[Symbol]:
    result: list[Symbol] = []
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if not value.isdigit() and value != ".":
                symbol = Symbol(location=(x, y), value=value)
                result.append(symbol)
    return result


if __name__ == "__main__":
    main()
