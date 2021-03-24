import math
import itertools
from collections import defaultdict

import aoc_search
import aoc_util
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
PLAYER_STATS = (10, 250) if TEST else (50, 500)
ENEMY_STATS = (14, 8) if TEST else (58, 9)


class EffectCreator:

    def __init__(
        self, 
        name, 
        cost, 
        turns,
        player_effect,
        enemy_effect,
        cleanup
    ):
        self.name = name
        self.cost = cost
        self.turns = turns
        self.player_effect = player_effect
        self.enemy_effect = enemy_effect
        self.cleanup = cleanup

    def create(self):
        return Effect(
            self.name,
            self.cost, 
            self.turns,
            self.player_effect,
            self.enemy_effect,
            self.cleanup
        )

class Effect:

    def __init__(
        self, 
        name, 
        cost, 
        turns,
        player_effect,
        enemy_effect,
        cleanup
    ):
        self.name = name
        self.cost = cost
        self.turns = turns
        self.player_effect = player_effect
        self.enemy_effect = enemy_effect
        self.cleanup = cleanup

    def apply(self, player, enemy):
        if self.player_effect is not None:
            self.player_effect(player)
        if self.enemy_effect is not None:
            self.enemy_effect(enemy)
        self.turns -= 1

    def clean(self, player):
        if self.cleanup is not None:
            self.cleanup(player)

    def active(self):
        return self.turns > 0

    def copy(self):
        return Effect(
            self.name,
            self.cost,
            self.turns,
            self.player_effect,
            self.enemy_effect,
            self.cleanup
        )

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name


SPELL_CREATORS = [
    EffectCreator(
        'Magic Missile',
        53,
        1,
        None,
        lambda enemy: enemy.boost_hp(-4),
        None
    ),
    EffectCreator(
        'Drain',
        73,
        1,
        lambda player: player.boost_hp(2),
        lambda enemy: enemy.boost_hp(-2),
        None
    ),
    EffectCreator(
        'Shield',
        113,
        6,
        lambda player: player.boost_armor(7),
        None,
        lambda player: player.boost_armor(-7),
    ),
    EffectCreator(
        'Poison',
        173,
        6,
        None,
        lambda enemy: enemy.boost_hp(-3),
        None
    ),
    EffectCreator(
        'Recharge',
        229,
        5,
        lambda player: player.boost_mana(101),
        None,
        None
    )
]


class Wizard:

    def __init__(self, hp, mana, armor=0):
        self.hp = hp
        self.mana = mana
        self.armor = armor

    def boost_hp(self, amount):
        self.hp += amount

    def boost_mana(self, amount):
        self.mana += amount

    def boost_armor(self, amount):
        if self.armor == 0 or amount < 0:
            self.armor += amount

    def cast(self, spell):
        self.mana -= spell.cost

    def can_perform(self, spell):
        return spell.cost <= self.mana

    def alive(self):
        return self.hp > 0

    def copy(self):
        return Wizard(
            self.hp,
            self.mana,
            self.armor
        )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {}'.format(self.hp, self.mana)


class Warlock:

    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def boost_hp(self, amount):
        self.hp += amount

    def attack(self, opponent):
        damage_dealt = self.damage - opponent.armor
        damage_dealt = max(1, damage_dealt)
        opponent.hp -= damage_dealt

    def alive(self):
        return self.hp > 0

    def copy(self):
        return Warlock(
            self.hp,
            self.damage
        )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {}'.format(self.hp, self.damage)


class Game:

    def __init__(self, player, enemy, hard, effects=None):
        self.player = player
        self.enemy = enemy
        self.hard = hard
        self.effects = set() if effects is None else effects

    def done(self):
        return not self.enemy.alive()

    def get_moves(self, mana_used):
        if not self.player.alive():
            return []

        can_perform = []
        for spell_creator in SPELL_CREATORS:
            if self.can_perform(spell_creator):
                can_perform.append(spell_creator.create())

        adjacent = []
        for spell in can_perform:
            total_used = spell.cost + mana_used
            game_copy = self.copy()
            game_copy.move(spell)
            adjacent.append((total_used, game_copy))
        return adjacent

    def can_perform(self, spell_creator):
        if not self.player.can_perform(spell_creator):
            return False
        spell = spell_creator.create()
        if spell not in self.effects:
            return True
        active_spell = self.get_active_spell(spell.name)
        return active_spell.turns == 1

    def get_active_spell(self, name):
        for spell in self.effects:
            if spell.name == name:
                return spell

    def move(self, spell):
        self.run_hard_mode()
        self.run_effects()
        self.player.cast(spell)
        self.effects.add(spell)

        self.run_hard_mode()
        self.run_effects()
        self.enemy.attack(self.player)

    def run_hard_mode(self):
        if self.hard:
            self.player.boost_hp(-1)
        return self.player.alive()

    def run_effects(self):
        to_deactivate = self.apply_effects()
        self.deactivate(to_deactivate)

    def apply_effects(self):
        to_deactivate = []
        for effect in self.effects:
            effect.apply(self.player, self.enemy)
            if not effect.active():
                to_deactivate.append(effect)
        return to_deactivate

    def deactivate(self, to_deactivate):
        for effect in to_deactivate:
            effect.clean(self.player)
            self.effects.remove(effect)

    def copy(self):
        return Game(
            self.player.copy(),
            self.enemy.copy(),
            self.hard,
            set([effect.copy() for effect in self.effects])
        )

    def __lt__(self, o):
        return self.player.hp > o.player.hp


def main():
    # Part 1 = 1269
    play_game(False)
    # Part 2 = 1309
    play_game(True)


def play_game(hard):
    game = Game(
        Wizard(*PLAYER_STATS), 
        Warlock(*ENEMY_STATS),
        hard
    )
    print(aoc_search.bfs(
        (0, game),
        lambda current: current.done(),
        lambda mana_used, current: current.get_moves(mana_used)
    ))


if __name__ == '__main__':
    main()

