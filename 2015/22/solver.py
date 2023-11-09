from dataclasses import dataclass
from typing import Optional, Self

from aoc import answer, search
from aoc.parser import Parser


@dataclass(unsafe_hash=True, order=True)
class Character:
    hp: int
    attack: int
    armor: int

    def add(self, values: tuple[int, int, int]) -> None:
        self.hp += values[0]
        self.attack += values[1]
        self.armor += values[2]

    def copy(self) -> Self:
        return Character(self.hp, self.attack, self.armor)


@dataclass(frozen=True)
class SpellEffect:
    boost: tuple[int, int, int]
    player: tuple[int, int, int]
    enemy: tuple[int, int, int]

    def setup(self, player: Character) -> None:
        player.add(self.boost)

    def turn(self, player: Character, enemy: Character) -> None:
        player.add(self.player)
        enemy.add(self.enemy)

    def cleanup(self, player: Character) -> None:
        player.add((-self.boost[0], -self.boost[1], -self.boost[2]))


EFFECTS: dict[str, SpellEffect] = {
    "Magic Missile": SpellEffect(boost=(0, 0, 0), player=(0, 0, 0), enemy=(-4, 0, 0)),
    "Drain": SpellEffect(boost=(0, 0, 0), player=(2, 0, 0), enemy=(-2, 0, 0)),
    "Shield": SpellEffect(boost=(0, 0, 7), player=(0, 0, 0), enemy=(0, 0, 0)),
    "Poison": SpellEffect(boost=(0, 0, 0), player=(0, 0, 0), enemy=(-3, 0, 0)),
    "Recharge": SpellEffect(boost=(0, 0, 0), player=(0, 101, 0), enemy=(0, 0, 0)),
}


@dataclass(unsafe_hash=True)
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


@dataclass(frozen=True, order=True)
class Game:
    player: Character
    enemy: Character
    damage: int
    spells: frozenset[Spell]

    def get_moves(self) -> list[tuple[int, Self]]:
        if self.player.hp <= 0:
            return []

        spells = []
        for spell in SPELL_BOOK:
            if self.can_perform(spell):
                spells.append(spell.copy())

        adjacent = []
        for spell in spells:
            adjacent.append((spell.cost, self.move(spell)))
        return adjacent

    def can_perform(self, spell: Spell) -> bool:
        if self.player.attack < spell.cost:
            return False
        for active_spell in self.spells:
            if active_spell.name == spell.name:
                if active_spell.turns > 1:
                    return False
        return True

    def move(self, spell: Spell) -> Self:
        player, enemy = self.player.copy(), self.enemy.copy()
        spells = [spell.copy() for spell in self.spells]

        player.hp -= self.damage
        Game.run_spells(player, enemy, spells)

        spell.setup(player)
        player.attack -= spell.cost
        spells.append(spell)

        player.hp -= self.damage
        Game.run_spells(player, enemy, spells)
        player.hp -= max(1, enemy.attack - player.armor)

        return Game(player, enemy, self.damage, frozenset(spells))

    @staticmethod
    def run_spells(player: Character, enemy: Character, spells: list[Spell]) -> None:
        inactive: list[Spell] = []
        for spell in spells:
            spell.apply(player, enemy)
            if spell.turns == 0:
                inactive.append(spell)

        for spell in inactive:
            spell.cleanup(player)
            spells.remove(spell)


def main() -> None:
    lines = Parser().lines()
    hp, attack = int(lines[0].split()[-1]), int(lines[1].split()[-1])
    answer.part1(1269, play_game(hp, attack, 0))
    answer.part2(1309, play_game(hp, attack, 1))


def play_game(hp: int, attack: int, damage: int) -> Optional[int]:
    game = Game(Character(50, 500, 0), Character(hp, attack, 0), damage, frozenset())
    return search.bfs_complete(
        (0, game),
        lambda current: current.enemy.hp <= 0,
        lambda current: current.get_moves(),
    )


if __name__ == "__main__":
    main()
