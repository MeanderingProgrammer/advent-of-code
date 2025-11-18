import re
from dataclasses import dataclass
from typing import Callable, Self

from aoc import answer
from aoc.parser import Parser


def in_range(value: int, minimum: int, maximum: int) -> bool:
    return value >= minimum and value <= maximum


def birth_year(value: str) -> bool:
    return in_range(int(value), 1920, 2002)


def issue_year(value: str) -> bool:
    return in_range(int(value), 2010, 2020)


def experation_year(value: str) -> bool:
    return in_range(int(value), 2020, 2030)


def height(value: str) -> bool:
    height = int(value[:-2])
    unit = value[-2:]
    if unit == "cm":
        return in_range(height, 150, 193)
    elif unit == "in":
        return in_range(height, 59, 76)
    else:
        return False


def hair_color(value: str) -> bool:
    expression = "^#[0-9,a-f]{6}$"
    match = re.search(expression, value)
    return match is not None


def eye_color(value: str) -> bool:
    return value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def passport_id(value: str) -> bool:
    expression = "^[0-9]{9}$"
    match = re.search(expression, value)
    return match is not None


FIELD_VALIDATORS: dict[str, Callable[[str], bool]] = {
    "byr": birth_year,
    "iyr": issue_year,
    "eyr": experation_year,
    "hgt": height,
    "hcl": hair_color,
    "ecl": eye_color,
    "pid": passport_id,
}


@dataclass(frozen=True)
class Passport:
    data: dict[str, str]

    @classmethod
    def new(cls, lines: list[str]) -> Self:
        data: dict[str, str] = dict()
        for line in lines:
            for part in line.split():
                key, value = part.split(":")
                data[key] = value
        return cls(data)

    def validate(self, run_validation: bool) -> bool:
        for field, validator in FIELD_VALIDATORS.items():
            if field not in self.data:
                return False
            if run_validation and not validator(self.data[field]):
                return False
        return True


@answer.timer
def main() -> None:
    passports = [Passport.new(group) for group in Parser().line_groups()]
    answer.part1(200, sum([passport.validate(False) for passport in passports]))
    answer.part2(116, sum([passport.validate(True) for passport in passports]))


if __name__ == "__main__":
    main()
