from aoc import answer
from aoc.parser import Parser


CHECKS = {
    "cats": lambda x, y: x > y,
    "trees": lambda x, y: x > y,
    "pomeranians": lambda x, y: x < y,
    "goldfish": lambda x, y: x < y,
}


class Match:
    def __init__(self, values):
        self.properties = {}
        for value in values:
            value = value.split(": ")
            self.properties[value[0]] = int(value[1])

    def does_match(self, aunt, calibrate):
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


class Aunt:
    def __init__(self, value):
        self.id, raw_properties = value.split(": ", 1)
        self.properties = {}
        for raw_property in raw_properties.split(", "):
            raw_property = raw_property.split(": ")
            self.properties[raw_property[0]] = int(raw_property[1])

    def get_number(self):
        return int(self.id.split()[1])


def main():
    answer.part1(213, get_aunt(False))
    answer.part2(323, get_aunt(True))


def get_aunt(calibrate):
    match, aunts = get_data()
    for aunt in aunts:
        matches = match.does_match(aunt, calibrate)
        if matches:
            return aunt.get_number()


def get_data():
    groups = Parser().line_groups()
    return Match(groups[0]), [Aunt(value) for value in groups[1]]


if __name__ == "__main__":
    main()
