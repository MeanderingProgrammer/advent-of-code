import commons.answer as answer
from commons.aoc_parser import Parser


class Polymer:

    def __init__(self, units):
        self.units = units

    def get_unit_types(self):
        unit_types = set()
        for unit in self.units:
            unit_types.add(unit.lower())
        return unit_types

    def remove_unit_type(self, unit_type):
        new_polymer_units = ''
        for unit in self.units:
            if unit.lower() != unit_type:
                new_polymer_units += unit
        return Polymer(new_polymer_units)

    def react(self):
        reaction_index = self.get_reaction_index()
        while reaction_index is not None:
            self.units = self.units[:reaction_index] + self.units[reaction_index+2:]
            reaction_index = self.get_reaction_index(reaction_index)

    def get_reaction_index(self, previous=None):
        start = 0 if previous is None else previous
        for i, unit in enumerate(self.units[start:-1]):
            next_unit = self.units[start + i + 1]
            if self.collide(unit, next_unit):
                return start + i
        return None if previous is None else self.get_reaction_index()

    def __len__(self):
        return len(self.units)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.units)

    @staticmethod
    def collide(unit, next_unit):
        if unit.islower() and next_unit.islower():
            return False
        if unit.isupper() and next_unit.isupper():
            return False
        return unit.lower() == next_unit.lower()


def main():
    polymer = Polymer(Parser().string())
    answer.part1(11242, solve_part_1(polymer))
    answer.part2(5492, solve_part_2(polymer))


def solve_part_1(polymer):
    polymer.react()
    return len(polymer)


def solve_part_2(polymer):
    lengths = []
    unit_types = polymer.get_unit_types()
    for unit_type in unit_types:
        new_polymer = polymer.remove_unit_type(unit_type)
        new_polymer.react()
        lengths.append(len(new_polymer))
    return min(lengths)


if __name__ == '__main__':
    main()
