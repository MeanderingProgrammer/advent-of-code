from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser
from aoc.search import Dijkstra


@dataclass(frozen=True, order=True, slots=True)
class Stats:
    hp: int = 0
    attack: int = 0
    armor: int = 0

    def dead(self) -> bool:
        return self.hp <= 0

    def add(self, other: Self) -> Self:
        return type(self)(
            hp=self.hp + other.hp,
            attack=self.attack + other.attack,
            armor=self.armor + other.armor,
        )

    def subtract(self, other: Self) -> Self:
        return type(self)(
            hp=self.hp - other.hp,
            attack=self.attack - other.attack,
            armor=self.armor - other.armor,
        )


@dataclass(frozen=True)
class Effect:
    cost: int
    boost: Stats = Stats()
    player: Stats = Stats()
    enemy: Stats = Stats()

    def setup(self, player: Stats) -> Stats:
        return player.add(self.boost)

    def turn(self, player: Stats, enemy: Stats) -> tuple[Stats, Stats]:
        return player.add(self.player), enemy.add(self.enemy)

    def cleanup(self, player: Stats) -> Stats:
        return player.subtract(self.boost)


EFFECTS: dict[str, Effect] = {
    "Magic Missile": Effect(cost=53, enemy=Stats(hp=-4)),
    "Drain": Effect(cost=73, player=Stats(hp=2), enemy=Stats(hp=-2)),
    "Shield": Effect(cost=113, boost=Stats(armor=7)),
    "Poison": Effect(cost=173, enemy=Stats(hp=-3)),
    "Recharge": Effect(cost=229, player=Stats(attack=101)),
}


@dataclass(frozen=True)
class Spell:
    name: str
    turns: int

    def effect(self) -> Effect:
        return EFFECTS[self.name]

    def move(self) -> Self:
        return type(self)(self.name, self.turns - 1)


SPELLS = [
    Spell(name="Magic Missile", turns=1),
    Spell(name="Drain", turns=1),
    Spell(name="Shield", turns=6),
    Spell(name="Poison", turns=6),
    Spell(name="Recharge", turns=5),
]


@dataclass(frozen=True, order=True)
class Game:
    player: Stats
    enemy: Stats
    damage: Stats
    spells: frozenset[Spell]

    def get_moves(self) -> list[tuple[int, Self]]:
        if self.player.dead():
            return []
        result: list[tuple[int, Self]] = []
        for spell in SPELLS:
            if self.can_perform(spell):
                result.append((spell.effect().cost, self.move(spell)))
        return result

    def can_perform(self, spell: Spell) -> bool:
        if self.player.attack < spell.effect().cost:
            return False
        for active_spell in self.spells:
            if active_spell.name == spell.name:
                if active_spell.turns > 1:
                    return False
        return True

    def move(self, spell: Spell) -> Self:
        player, enemy, spells = self.player, self.enemy, list(self.spells)

        player = player.subtract(self.damage)
        player, enemy, spells = Game.run_spells(player, enemy, spells)

        player = player.subtract(Stats(attack=spell.effect().cost))
        player = spell.effect().setup(player)
        spells.append(spell)

        player = player.subtract(self.damage)
        player, enemy, spells = Game.run_spells(player, enemy, spells)
        player = player.subtract(Stats(hp=max(1, enemy.attack - player.armor)))

        return type(self)(player, enemy, self.damage, frozenset(spells))

    @staticmethod
    def run_spells(
        player: Stats, enemy: Stats, spells: list[Spell]
    ) -> tuple[Stats, Stats, list[Spell]]:
        active_spells: list[Spell] = []
        for spell in spells:
            player, enemy = spell.effect().turn(player, enemy)
            spell = spell.move()
            if spell.turns == 0:
                player = spell.effect().cleanup(player)
            else:
                active_spells.append(spell)
        return player, enemy, active_spells


@answer.timer
def main() -> None:
    lines = Parser().lines()
    hp, attack = int(lines[0].split()[-1]), int(lines[1].split()[-1])
    answer.part1(1269, play_game(hp, attack, 0))
    answer.part2(1309, play_game(hp, attack, 1))


def play_game(hp: int, attack: int, damage: int) -> int | None:
    start = Game(
        player=Stats(hp=50, attack=500),
        enemy=Stats(hp=hp, attack=attack),
        damage=Stats(hp=damage),
        spells=frozenset(),
    )
    search: Dijkstra[Game] = Dijkstra(
        start=start,
        done=lambda game: game.enemy.dead(),
        neighbors=lambda game: game.get_moves(),
    )
    return search.run()


if __name__ == "__main__":
    main()
