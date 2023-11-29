from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser

CHECKS = dict(
    cats=lambda x, y: x > y,
    trees=lambda x, y: x > y,
    pomeranians=lambda x, y: x < y,
    goldfish=lambda x, y: x < y,
)


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
            if calibrate:
                check = CHECKS.get(name, lambda x, y: x == y)
            else:
                check = lambda x, y: x == y
            if not check(aunt_value, value):
                return False
        return True


def main() -> None:
    groups = Parser().line_groups()
    match, aunts = get_match(groups[0]), get_aunts(groups[1])
    answer.part1(213, get_aunt(match, aunts, False))
    answer.part2(323, get_aunt(match, aunts, True))


def get_match(lines: list[str]) -> Match:
    properties: dict[str, int] = dict()
    for line in lines:
        key, amount = line.split(": ")
        properties[key] = int(amount)
    return Match(properties)


def get_aunts(lines: list[str]) -> list[Aunt]:
    def parse_aunt(line: str) -> Aunt:
        id, raw_properties = line.split(": ", 1)
        properties: dict[str, int] = dict()
        for property in raw_properties.split(", "):
            key, amount = property.split(": ")
            properties[key] = int(amount)
        return Aunt(
            id=int(id.split()[1]),
            properties=properties,
        )

    return [parse_aunt(line) for line in lines]


def get_aunt(match: Match, aunts: list[Aunt], calibrate: bool) -> int:
    for aunt in aunts:
        if match.does_match(aunt, calibrate):
            return aunt.id
    raise Exception("Failed")


if __name__ == "__main__":
    main()
