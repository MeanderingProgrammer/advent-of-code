import itertools
from collections.abc import Generator
from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Item:
    name: str
    cost: int
    damage: int
    armor: int


@dataclass(frozen=True)
class Inventory:
    weapons: list[Item]
    armors: list[Item]
    rings: list[Item]

    def permute(self) -> Generator[list[Item], None, None]:
        for weapons in Inventory.iter(self.weapons, [1]):
            for armors in Inventory.iter(self.armors, [0, 1]):
                for rings in Inventory.iter(self.rings, [0, 1, 2]):
                    yield weapons + armors + rings

    @staticmethod
    def iter(
        items: list[Item], lengths: list[int]
    ) -> Generator[list[Item], None, None]:
        for length in lengths:
            for item in itertools.combinations(items, length):
                yield list(item)


@dataclass
class Character:
    starting_hp: int
    hp: int
    damage: int
    armor: int
    items: list[Item]

    @property
    def alive(self):
        return self.hp > 0

    @property
    def total_damage(self) -> int:
        return self.damage + sum([item.damage for item in self.items])

    @property
    def total_armor(self):
        return self.armor + sum([item.armor for item in self.items])

    def set_items(self, items: list[Item]) -> None:
        self.hp = self.starting_hp
        self.items = items

    def attack(self, opponent: Self) -> None:
        damage = self.total_damage - opponent.total_armor
        opponent.hp -= max(damage, 1)


@answer.timer
def main() -> None:
    groups = Parser().line_groups()
    inventory = Inventory(
        weapons=get_items(groups[0]),
        armors=get_items(groups[1]),
        rings=get_items(groups[2]),
    )
    player = Character(starting_hp=100, hp=100, damage=0, armor=0, items=[])
    enemy = Character(
        starting_hp=int(groups[3][0].split()[-1]),
        hp=int(groups[3][0].split()[-1]),
        damage=int(groups[3][1].split()[-1]),
        armor=int(groups[3][2].split()[-1]),
        items=[],
    )

    win_costs: list[int] = []
    loss_costs: list[int] = []
    for items in inventory.permute():
        player.set_items(items)
        enemy.set_items([])
        cost = sum([item.cost for item in items])
        if fight(player, enemy):
            win_costs.append(cost)
        else:
            loss_costs.append(cost)

    answer.part1(121, min(win_costs))
    answer.part2(201, max(loss_costs))


def get_items(lines: list[str]) -> list[Item]:
    def parse_item(line: str) -> Item:
        parts = line.split()
        return Item(
            name=" ".join(parts[:-3]),
            cost=int(parts[-3]),
            damage=int(parts[-2]),
            armor=int(parts[-1]),
        )

    return [parse_item(line) for line in lines[1:]]


def fight(player: Character, enemy: Character) -> bool:
    while player.alive and enemy.alive:
        player.attack(enemy)
        enemy.attack(player)
    return not enemy.alive


if __name__ == "__main__":
    main()
