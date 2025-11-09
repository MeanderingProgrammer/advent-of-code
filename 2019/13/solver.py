from collections import defaultdict
from dataclasses import dataclass

from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser

TILE_MAPPING = {0: "empty", 1: "wall", 2: "block", 3: "horizontal paddle", 4: "ball"}


@dataclass
class Game:
    tile_buffer: list[int]
    tile_freq: dict[str, int]
    tile_x: dict[str, int]
    score: int = 0

    def active(self) -> bool:
        return True

    def get_input(self) -> int:
        diff = self.tile_x["ball"] - self.tile_x["horizontal paddle"]
        return min(1, max(-1, diff))

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


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    answer.part1(363, play_game(memory, False))
    answer.part2(17159, play_game(memory, True))


def play_game(memory: list[int], play_for_free: bool) -> int:
    memory = memory.copy()
    if play_for_free:
        memory[0] = 2
    game = Game([], defaultdict(int), dict())
    Computer(bus=game, memory=memory).run()
    return game.score if play_for_free else game.tile_freq["block"]


if __name__ == "__main__":
    main()
