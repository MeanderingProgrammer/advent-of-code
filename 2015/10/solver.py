from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass
class Game:
    value: list[int]

    def play(self) -> None:
        next_value: list[int] = []
        for i, current in enumerate(self.value):
            if i > 0 and current == self.value[i - 1]:
                next_value[-2] += 1
            else:
                next_value.extend([1, current])
        self.value = next_value


def main() -> None:
    game = Game(list(map(int, Parser(strip=True).string())))
    answer.part1(360154, run(game, 40))
    answer.part2(5103798, run(game, 10))


def run(game: Game, rounds: int) -> int:
    for _ in range(rounds):
        game.play()
    return len(game.value)


if __name__ == "__main__":
    main()
