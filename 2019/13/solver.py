from collections import defaultdict

from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser

TILE_MAPPING = {0: "empty", 1: "wall", 2: "block", 3: "horizontal paddle", 4: "ball"}


class Game:
    def __init__(self, memory: list[int]):
        self.computer = Computer(self)
        self.computer.set_memory(memory)

        self.tile_buffer: list[int] = []
        self.tile_freq: dict[str, int] = defaultdict(int)
        self.tile_x: dict[str, int] = dict()
        self.score = 0

    def play(self) -> None:
        self.computer.run()

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


def main() -> None:
    answer.part1(363, play_game(False))
    answer.part2(17159, play_game(True))


def play_game(play_for_free: bool) -> int:
    memory = Parser().int_csv()
    if play_for_free:
        memory[0] = 2
    game = Game(memory)
    game.play()
    return game.score if play_for_free else game.tile_freq["block"]


if __name__ == "__main__":
    main()
