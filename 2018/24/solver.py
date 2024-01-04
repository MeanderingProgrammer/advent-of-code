import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Self

from aoc import answer
from aoc.parser import Parser


class Category(Enum):
    IMMUNE = auto()
    INFECTION = auto()


@dataclass
class Group:
    id: int
    category: Category
    units: int
    hp: int
    weaknesses: list[str]
    immunities: list[str]
    damage: int
    damage_type: str
    initiative: int

    @property
    def dead(self) -> bool:
        return self.units <= 0

    @property
    def power(self) -> int:
        return self.units * self.damage

    def calculate_damage(self, o: Self) -> int:
        if self.damage_type in o.immunities:
            multiplier = 0
        elif self.damage_type in o.weaknesses:
            multiplier = 2
        else:
            multiplier = 1
        return self.power * multiplier

    def hit(self, damage: int) -> None:
        self.units -= damage // self.hp

    def __eq__(self, o: Optional[Self]) -> bool:
        return o is not None and self.id == o.id


@dataclass
class Battle:
    groups: list[Group]

    def simulate(self) -> None:
        current, previous = None, 0
        while len(self.groups) > 0 and current != previous:
            self.attack()
            previous = current
            current = self.winning_units()

    def attack(self) -> None:
        assignments = self.assign_targets()
        assignments.sort(key=lambda assignment: assignment[0].initiative, reverse=True)
        for group, target in assignments:
            if group.dead:
                continue
            damage = group.calculate_damage(target)
            target.hit(damage)
            if target.dead:
                self.groups.remove(target)

    def assign_targets(self) -> list[tuple[Group, Group]]:
        assignments: list[tuple[Group, Group]] = []
        targets: list[Group] = []
        self.groups.sort(
            key=lambda group: (group.power, group.initiative), reverse=True
        )
        for group in self.groups:
            target = self.get_target(group, targets)
            if target is not None:
                assignments.append((group, target))
                targets.append(target)
        return assignments

    def get_target(self, group: Group, targets: list[Group]) -> Optional[Group]:
        opponents = {
            Category.IMMUNE: Category.INFECTION,
            Category.INFECTION: Category.IMMUNE,
        }[group.category]

        options = self.get_category(opponents)
        options = [option for option in options if option not in targets]
        options.sort(
            key=lambda option: (
                group.calculate_damage(option),
                option.power,
                option.initiative,
            ),
            reverse=True,
        )
        if len(options) == 0:
            return None
        else:
            return None if group.calculate_damage(options[0]) == 0 else options[0]

    def immune_won(self) -> bool:
        immune = self.get_category(Category.IMMUNE)
        infection = self.get_category(Category.INFECTION)
        return len(immune) > 0 and len(infection) == 0

    def get_category(self, category: Category) -> list[Group]:
        return [group for group in self.groups if group.category == category]

    def winning_units(self) -> int:
        return sum([group.units for group in self.groups])


@answer.timer
def main() -> None:
    answer.part1(16086, solve_part_1())
    answer.part2(3957, solve_part_2())


def solve_part_1() -> int:
    battle = get_battle(0)
    battle.simulate()
    return battle.winning_units()


def solve_part_2() -> int:
    immune_boost = 0
    while True:
        immune_boost += 1
        battle = get_battle(immune_boost)
        battle.simulate()
        if battle.immune_won():
            return battle.winning_units()


def get_battle(immune_boost: int) -> Battle:
    def parse_group(id: int, category: Category, raw: str, boost: int) -> Group:
        traits: dict[str, list[str]] = dict()
        match = re.search(r"\((.*)\)", raw)
        if match is not None:
            for raw_trait in match.group(1).split("; "):
                trait_type, trait_values = raw_trait.split(" to ")
                traits[trait_type] = trait_values.split(", ")
        parts = raw.split()
        return Group(
            id=id,
            category=category,
            units=int(parts[0]),
            hp=int(parts[4]),
            weaknesses=traits.get("weak", []),
            immunities=traits.get("immune", []),
            damage=int(parts[-6]) + boost,
            damage_type=parts[-5],
            initiative=int(parts[-1]),
        )

    immune, infection = Parser().line_groups()
    id, groups = 0, []
    for value in immune[1:]:
        groups.append(parse_group(id, Category.IMMUNE, value, immune_boost))
        id += 1
    for value in infection[1:]:
        groups.append(parse_group(id, Category.INFECTION, value, 0))
        id += 1
    return Battle(groups)


if __name__ == "__main__":
    main()
