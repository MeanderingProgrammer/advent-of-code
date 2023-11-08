from dataclasses import dataclass
from typing import Dict, List, Optional, Self, Tuple

from aoc import answer, search


@dataclass
class Character:
    hp: int
    attack: int
    armor: int

    def add(self, values: Tuple[int, int, int]) -> None:
        self.hp += values[0]
        self.attack += values[1]
        self.armor += values[2]

    def copy(self) -> Self:
        return Character(self.hp, self.attack, self.armor)


@dataclass(frozen=True)
class SpellEffect:
    boost: Tuple[int, int, int]
    player: Tuple[int, int, int]
    enemy: Tuple[int, int, int]

    def setup(self, player: Character) -> None:
        player.add(self.boost)

    def turn(self, player: Character, enemy: Character) -> None:
        player.add(self.player)
        enemy.add(self.enemy)

    def cleanup(self, player: Character) -> None:
        player.add((-self.boost[0], -self.boost[1], -self.boost[2]))


EFFECTS: Dict[str, SpellEffect] = {
    "Magic Missile": SpellEffect(boost=(0, 0, 0), player=(0, 0, 0), enemy=(-4, 0, 0)),
    "Drain": SpellEffect(boost=(0, 0, 0), player=(2, 0, 0), enemy=(-2, 0, 0)),
    "Shield": SpellEffect(boost=(0, 0, 7), player=(0, 0, 0), enemy=(0, 0, 0)),
    "Poison": SpellEffect(boost=(0, 0, 0), player=(0, 0, 0), enemy=(-3, 0, 0)),
    "Recharge": SpellEffect(boost=(0, 0, 0), player=(0, 101, 0), enemy=(0, 0, 0)),
}


@dataclass
class Spell:
    name: str
    cost: int
    turns: int

    def setup(self, player: Character) -> None:
        EFFECTS[self.name].setup(player)

    def apply(self, player: Character, enemy: Character) -> None:
        EFFECTS[self.name].turn(player, enemy)
        self.turns -= 1

    def cleanup(self, player: Character) -> None:
        EFFECTS[self.name].cleanup(player)

    def copy(self) -> Self:
        return Spell(self.name, self.cost, self.turns)


SPELL_BOOK = [
    Spell(name="Magic Missile", cost=53, turns=1),
    Spell(name="Drain", cost=73, turns=1),
    Spell(name="Shield", cost=113, turns=6),
    Spell(name="Poison", cost=173, turns=6),
    Spell(name="Recharge", cost=229, turns=5),
]


@dataclass(frozen=True)
class Game:
    player: Character
    enemy: Character
    player_damage: int
    spells: List[Spell]

    def get_moves(self, mana_used: int) -> List[Tuple[int, Self]]:
        if self.player.hp <= 0:
            return []

        spells = []
        for spell in SPELL_BOOK:
            if self.can_perform(spell):
                spells.append(spell.copy())

        adjacent = []
        for spell in spells:
            total_used = spell.cost + mana_used
            game_copy = self.copy()
            game_copy.move(spell)
            adjacent.append((total_used, game_copy))
        return adjacent

    def can_perform(self, spell: Spell) -> bool:
        if self.player.attack < spell.cost:
            return False
        for active_spell in self.spells:
            if active_spell.name == spell.name:
                if active_spell.turns > 1:
                    return False
        return True

    def move(self, spell: Spell) -> None:
        self.player.hp -= self.player_damage
        self.run_spells()

        spell.setup(self.player)
        self.player.attack -= spell.cost
        self.spells.append(spell)

        self.player.hp -= self.player_damage
        self.run_spells()
        self.player.hp -= max(1, self.enemy.attack - self.player.armor)

    def run_spells(self) -> None:
        inactive: List[Spell] = []
        for spell in self.spells:
            spell.apply(self.player, self.enemy)
            if spell.turns == 0:
                inactive.append(spell)

        for spell in inactive:
            spell.cleanup(self.player)
            self.spells.remove(spell)

    def copy(self):
        return Game(
            self.player.copy(),
            self.enemy.copy(),
            self.player_damage,
            [spell.copy() for spell in self.spells],
        )

    def __lt__(self, o):
        return self.player.hp > o.player.hp


def main() -> None:
    answer.part1(1269, play_game(0))
    answer.part2(1309, play_game(1))


def play_game(player_damage: int) -> Optional[int]:
    game = Game(Character(50, 500, 0), Character(58, 9, 0), player_damage, [])
    return search.bfs_complete(
        (0, game),
        lambda current: current.enemy.hp <= 0,
        lambda mana_used, current: current.get_moves(mana_used),
    )


if __name__ == "__main__":
    main()
