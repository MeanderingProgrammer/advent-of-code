from dataclasses import dataclass
from typing import Optional, Self

from aoc import answer
from aoc.parser import Parser


@dataclass
class Polymer:
    units: list[str]

    def react(self) -> int:
        reaction_index = self.get_reaction_index(None)
        while reaction_index is not None:
            del self.units[reaction_index]
            del self.units[reaction_index]
            reaction_index = self.get_reaction_index(reaction_index)
        return len(self.units)

    def get_reaction_index(self, previous: Optional[int]) -> Optional[int]:
        for i in range(previous or 0, len(self.units) - 1):
            u1, u2 = self.units[i], self.units[i + 1]
            if u1.islower() != u2.islower() and u1.lower() == u2.lower():
                return i
        return None if previous is None else self.get_reaction_index(None)

    def get_unit_types(self) -> set[str]:
        return set([unit.lower() for unit in set(self.units)])

    def remove_unit_type(self, unit_type: str) -> Self:
        return type(self)([unit for unit in self.units if unit.lower() != unit_type])


def main() -> None:
    polymer = Polymer([value for value in Parser().string()])
    answer.part1(11242, solve_part_1(polymer))
    answer.part2(5492, solve_part_2(polymer))


def solve_part_1(polymer: Polymer) -> int:
    return polymer.react()


def solve_part_2(polymer: Polymer) -> int:
    lengths = [
        polymer.remove_unit_type(unit_type).react()
        for unit_type in polymer.get_unit_types()
    ]
    return min(lengths)


if __name__ == "__main__":
    main()
