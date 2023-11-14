from collections import defaultdict
from dataclasses import dataclass
from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser

TILE_MAPPING = {0: "empty", 1: "wall", 2: "block", 3: "horizontal paddle", 4: "ball"}


@dataclass
class Game(Bus):
    tile_buffer: list[int]
    tile_freq: dict[str, int]
    tile_x: dict[str, int]
    score: int = 0

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        diff = self.tile_x["ball"] - self.tile_x["horizontal paddle"]
        return min(1, max(-1, diff))

    @override
    def add_output(self, value: int) -> None:
        self.tile_buffer.append(value)
        if len(self.tile_buffer) == 3:
            x, y, value = self.tile_buffer
            if x == -1 and y == 0:
                self.score = value
            else:
                name = TILE_MAPPING[value]
                self.tile_freq[name] += 1
                self.tile_x[name] = x
            self.tile_buffer = []


def main() -> None:
    answer.part1(363, play_game(False))
    answer.part2(17159, play_game(True))


def play_game(play_for_free: bool) -> int:
    memory = Parser().int_csv()
    if play_for_free:
        memory[0] = 2
    game = Game([], defaultdict(int), dict())
    Computer(bus=game, memory=memory).run()
    return game.score if play_for_free else game.tile_freq["block"]


if __name__ == "__main__":
    main()
