from dataclasses import dataclass
from enum import Enum, auto

from aoc import answer
from aoc.parser import Parser


class Check(Enum):
    EQUAL = auto()
    GREATER = auto()
    LESS = auto()

    def valid(self, v1: int, v2: int) -> bool:
        match self:
            case Check.EQUAL:
                return v1 == v2
            case Check.GREATER:
                return v1 > v2
            case Check.LESS:
                return v1 < v2


@dataclass(frozen=True)
class Aunt:
    id: int
    properties: dict[str, int]


@dataclass(frozen=True)
class Match:
    properties: dict[str, int]

    def does_match(self, aunt: Aunt, calibrate: bool) -> bool:
        for name, value in self.properties.items():
            aunt_value = aunt.properties.get(name)
            if aunt_value is None:
                continue
            check = Check.EQUAL
            if calibrate:
                if name in ["cats", "trees"]:
                    check = Check.GREATER
                if name in ["pomeranians", "goldfish"]:
                    check = Check.LESS
            if not check.valid(aunt_value, value):
                return False
        return True


@answer.timer
def main() -> None:
    groups = Parser().line_groups()
    match = get_match(groups[0])
    aunts = [get_aunt(line) for line in groups[1]]
    answer.part1(213, find(match, aunts, False))
    answer.part2(323, find(match, aunts, True))


def get_match(lines: list[str]) -> Match:
    properties: dict[str, int] = dict()
    for line in lines:
        key, amount = line.split(": ")
        properties[key] = int(amount)
    return Match(properties)


def get_aunt(line: str) -> Aunt:
    id, raw_properties = line.split(": ", 1)
    properties: dict[str, int] = dict()
    for property in raw_properties.split(", "):
        key, amount = property.split(": ")
        properties[key] = int(amount)
    return Aunt(
        id=int(id.split()[1]),
        properties=properties,
    )


def find(match: Match, aunts: list[Aunt], calibrate: bool) -> int:
    for aunt in aunts:
        if match.does_match(aunt, calibrate):
            return aunt.id
    raise Exception("Failed")


if __name__ == "__main__":
    main()
