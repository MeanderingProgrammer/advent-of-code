import math
import itertools
from collections import defaultdict

import aoc_search
import aoc_util
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class Character:

    def __init__(self, hp, damage, armor):
        self.starting_hp = hp
        self.items = []

        self.hp = hp
        self.damage = damage
        self.armor = armor

    def attack(self, opponent):
        damage = self.get_damage() - opponent.get_armor()
        damage = max(damage, 1)
        opponent.hp -= damage

    def get_damage(self):
        damage = self.damage
        for item in self.items:
            damage += item.damage
        return damage

    def get_armor(self):
        armor = self.armor
        for item in self.items:
            armor += item.armor
        return armor

    def alive(self):
        return self.hp > 0

    def set_items(self, items):
        self.items = items

    def reset(self):
        self.hp = self.starting_hp
        self.items = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} {} {}'.format(self.hp, self.damage, self.armor)


class Item:

    def __init__(self, raw):
        parts = raw.split()
        self.name = ' '.join(parts[:-3])
        self.cost = int(parts[-3])
        self.damage = int(parts[-2])
        self.armor = int(parts[-1])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {} {} {}'.format(self.name, self.cost, self.damage, self.armor)


def main():
    player = Character(100, 0, 0)
    enemy, weapons, armors, rings = get_data()

    win_costs, loss_costs = [], []
    for items in permute(weapons, armors, rings):
        player.set_items(items)
        win = fight(player, enemy)
        data = win_costs if win else loss_costs
        data.append(sum([item.cost for item in items]))
        player.reset()
        enemy.reset()
        
    # Part 1 = 121
    print(min(win_costs))
    # Part 2 = 201
    print(max(loss_costs))


def fight(player, enemy):
    while player.alive() and enemy.alive():
        player.attack(enemy)
        enemy.attack(player)
    return not enemy.alive()


def permute(weapons, armors, rings):
    for weapon in iter(weapons, [1]):
        for armor in iter(armors, [0, 1]):
            for ring in iter(rings, [0, 1, 2]):
                yield list(weapon) + list(armor) + list(ring)


def iter(items, lengths):
    for length in lengths:
        for item in itertools.combinations(items, length):
            yield item


def get_data():
    groups = Parser(FILE_NAME).line_groups()
    weapons = get_items(groups[0])
    armors = get_items(groups[1])
    rings = get_items(groups[2])
    enemy =get_character(groups[3])
    return enemy, weapons, armors, rings


def get_items(items):
    return [Item(item) for item in items[1:]]


def get_character(stats):
    return Character(
        int(stats[0].split()[-1]),
        int(stats[1].split()[-1]),
        int(stats[2].split()[-1])
    )


if __name__ == '__main__':
    main()

