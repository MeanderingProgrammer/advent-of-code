from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Dict, List, Optional, Set, Tuple

from aoc import answer
from aoc.board import Point
from aoc.parser import Parser


class Team(Enum):
    GOBLIN = auto()
    ELF = auto()


@dataclass
class Character:
    team: Team
    position: Point
    damage: int
    hp: int = 200

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def attack(self, target: "Character") -> None:
        target.hp -= self.damage

    def find_target(self, opponents: List["Character"]) -> Optional["Character"]:
        reach = self.position.adjacent()
        targets = [opponent for opponent in opponents if opponent.position in reach]
        if len(targets) == 0:
            return None
        return min(targets, key=lambda character: (character.hp, character.position))


@dataclass
class Game:
    open_path: Set[Point]
    characters: List[Character]
    until_elf_death: bool

    def play(self) -> Optional[int]:
        round = 0
        while True:
            status = self.round()
            if status is None:
                return None
            if not status:
                break
            round += 1
        return round * sum([character.hp for character in self.characters])

    def round(self) -> Optional[bool]:
        ordered = sorted(self.characters, key=lambda character: character.position)
        for character in ordered:
            if character.alive:
                status = self.move(character)
                if not status:
                    return status
        return True

    def move(self, character: Character) -> Optional[bool]:
        opponents = [
            opponent for opponent in self.characters if opponent.team != character.team
        ]
        if len(opponents) == 0:
            return False

        target = character.find_target(opponents)
        if target is None:
            move = self.get_move(character, opponents)
            if move is not None:
                character.position = move
                target = character.find_target(opponents)

        if target is not None:
            character.attack(target)
            if not target.alive:
                self.characters.remove(target)
                if self.until_elf_death and target.team == Team.ELF:
                    return None
        return True

    def get_move(
        self, character: Character, opponents: List[Character]
    ) -> Optional[Point]:
        occupied = set([other.position for other in self.characters])

        def get_adjacent(point: Point) -> List[Point]:
            result = []
            for adjacent in point.adjacent():
                if adjacent in self.open_path and adjacent not in occupied:
                    result.append(adjacent)
            return result

        targets = []
        for opponent in opponents:
            targets.extend(get_adjacent(opponent.position))
        distances = self.calculate_distances(character.position, get_adjacent)

        target_distances = [
            (distances[point][0], point) for point in targets if point in distances
        ]
        if len(target_distances) == 0:
            return None
        closest = min(target_distances)[1]
        while distances[closest][0] > 1:
            closest = distances[closest][1]
        return closest

    def calculate_distances(
        self,
        start: Point,
        get_adjacent: Callable[[Point], List[Point]],
    ) -> Dict[Point, Tuple[int, Point]]:
        queue: List[Tuple[int, Point]] = [(0, start)]
        distances: Dict[Point, Tuple[int, Point]] = {start: (0, start)}
        while len(queue) > 0:
            length, point = queue.pop(0)
            for adjacent in get_adjacent(point):
                if adjacent not in distances:
                    queue.append((length + 1, adjacent))
                parent_distance = (length + 1, point)
                if adjacent not in distances or distances[adjacent] > parent_distance:
                    distances[adjacent] = parent_distance
        return distances


def main() -> None:
    data = Parser().nested_lines()
    answer.part1(214731, play_game(data, False))
    answer.part2(53222, play_game(data, True))


def play_game(data: List[List[str]], until_win: bool) -> int:
    elf_damage = 10 if until_win else 3
    while True:
        result = get_game(data, elf_damage, until_win).play()
        if result is not None:
            return result
        elf_damage += 1


def get_game(data: List[List[str]], elf_damage: int, until_elf_death: bool) -> Game:
    return Game(
        open_path=get_open_path(data),
        characters=get_characters(data, elf_damage),
        until_elf_death=until_elf_death,
    )


def get_open_path(data: List[List[str]]) -> Set[Point]:
    open_path = set()
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value != "#":
                point = Point(x, y)
                open_path.add(point)
    return open_path


def get_characters(data: List[List[str]], elf_damage: int) -> List[Character]:
    traits_mapping = dict(
        G=(Team.GOBLIN, 3),
        E=(Team.ELF, elf_damage),
    )
    characters = []
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value in traits_mapping:
                traits = traits_mapping[value]
                characters.append(
                    Character(team=traits[0], position=Point(x, y), damage=traits[1])
                )
    return characters


if __name__ == "__main__":
    main()
