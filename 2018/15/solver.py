from aoc import answer, search
from aoc.board import Point
from aoc.parser import Parser
from dataclasses import dataclass
from operator import attrgetter
from typing import Callable, List, Optional, Set


@dataclass
class Character:
    symbol: str
    position: Point
    damage: int
    hp: int = 200

    def attack(self, target: "Character") -> None:
        target.hp -= self.damage

    def find_target(self, opponents: List["Character"]) -> Optional["Character"]:
        reach = self.position.adjacent()
        targets = [opponent for opponent in opponents if opponent.position in reach]
        targets.sort(key=attrgetter("hp", "position"))
        return None if len(targets) == 0 else targets[0]

    def alive(self) -> bool:
        return self.hp > 0

    def __lt__(self, o):
        return self.position < o.position


@dataclass
class Game:
    open_path: Set[Point]
    goblins: List[Character]
    elves: List[Character]
    round_num: int = 0

    def play(self) -> int:
        while True:
            if not self.make_move():
                break
            self.round_num += 1
        return self.get_result()

    def play_until_elf_dies(self) -> Optional[int]:
        initial_elves = len(self.elves)
        while True:
            if not self.make_move():
                break
            if len(self.elves) != initial_elves:
                return None
            self.round_num += 1
        return self.get_result()

    def get_result(self) -> int:
        hps = [character.hp for character in self.characters()]
        return self.round_num * sum(hps)

    def make_move(self) -> bool:
        for character in self.characters():
            if not character.alive():
                continue

            opponents = self.elves if character.symbol == "G" else self.goblins
            if len(opponents) == 0:
                return False

            target = character.find_target(opponents)
            if target is None:
                move = self.get_move(character, opponents)
                if move is not None:
                    character.position = move
                target = character.find_target(opponents)

            if target is None:
                continue
            character.attack(target)
            if not target.alive():
                opponents.remove(target)
        return True

    def characters(self) -> List[Character]:
        characters = self.goblins + self.elves
        characters.sort()
        return characters

    def get_move(
        self, character: Character, opponents: List[Character]
    ) -> Optional[Point]:
        occupied = set([other.position for other in self.characters()])

        def get_adjacent(point: Point) -> List[Point]:
            result = []
            for adjacent in point.adjacent():
                if adjacent in self.open_path and adjacent not in occupied:
                    result.append(adjacent)
            return result

        opponent_adjacent = []
        for opponent in opponents:
            opponent_adjacent.extend(get_adjacent(opponent.position))

        closest = self.closest(character.position, opponent_adjacent, get_adjacent)
        if closest is not None:
            return self.closest(closest, get_adjacent(character.position), get_adjacent)
        return None

    def closest(
        self,
        start: Point,
        options: List[Point],
        get_adjacent: Callable[[Point], List[Point]],
    ) -> Optional[Point]:
        distances = dict()
        for option in options:
            distance = search.bfs(start, option, get_adjacent)
            if distance is not None:
                distances[option] = distance

        if len(distances) == 0:
            return None

        min_dist = min(distances.values())
        minimums = [
            point for point, distance in distances.items() if distance == min_dist
        ]
        minimums.sort()
        return minimums[0]


def main() -> None:
    data = Parser().nested_lines()
    answer.part1(214731, play_game(data, False))
    answer.part2(53222, play_game(data, True))


def play_game(data: List[List[str]], until_win: bool) -> int:
    if until_win:
        elf_damage, result = 10, None
        while result is None:
            elf_damage += 1
            game = get_game(data, elf_damage)
            result = game.play_until_elf_dies()
        return result
    else:
        game = get_game(data, 3)
        return game.play()


def get_game(data: List[List[str]], elf_damage: int) -> Game:
    return Game(
        open_path=get_open_path(data),
        goblins=get_characters(data, "G", 3),
        elves=get_characters(data, "E", elf_damage),
    )


def get_open_path(data: List[List[str]]) -> Set[Point]:
    open_path = set()
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value != "#":
                point = Point(x, y)
                open_path.add(point)
    return open_path


def get_characters(data: List[List[str]], symbol: str, damage: int) -> List[Character]:
    characters = []
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == symbol:
                character = Character(
                    symbol=symbol, position=Point(x, y), damage=damage
                )
                characters.append(character)
    return characters


if __name__ == "__main__":
    main()
