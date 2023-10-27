import re

from aoc import answer
from aoc.parser import Parser


def in_range(value, minimum, maximum):
    return value >= minimum and value <= maximum


def birth_year(value):
    value = int(value)
    return in_range(value, 1920, 2002)


def issue_year(value):
    value = int(value)
    return in_range(value, 2010, 2020)


def experation_year(value):
    value = int(value)
    return in_range(value, 2020, 2030)


def height(value):
    height = int(value[:-2])
    unit = value[-2:]
    if unit == "cm":
        return in_range(height, 150, 193)
    elif unit == "in":
        return in_range(height, 59, 76)
    else:
        return False


def hair_color(value):
    expression = "^#[0-9,a-f]{6}$"
    match = re.search(expression, value)
    return match is not None


def eye_color(value):
    valid = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    return value in valid


def passport_id(value):
    expression = "^[0-9]{9}$"
    match = re.search(expression, value)
    return match is not None


FIELD_VALIDATORS = {
    "byr": birth_year,
    "iyr": issue_year,
    "eyr": experation_year,
    "hgt": height,
    "hcl": hair_color,
    "ecl": eye_color,
    "pid": passport_id,
}


class Passport:
    def __init__(self, lines):
        self.data = {}
        for line in lines:
            for part in line.split():
                kv = part.split(":")
                self.data[kv[0]] = kv[1]

    def validate(self, run_validation):
        for field in FIELD_VALIDATORS:
            if field not in self.data:
                return False
            validator = FIELD_VALIDATORS[field]
            value = self.data[field]
            if run_validation and not validator(value):
                return False
        return True


def main():
    passports = get_passports()
    answer.part1(200, sum([passport.validate(False) for passport in passports]))
    answer.part2(116, sum([passport.validate(True) for passport in passports]))


def get_passports():
    return [Passport(group) for group in Parser().line_groups()]


if __name__ == "__main__":
    main()
