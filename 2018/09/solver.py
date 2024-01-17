from collections import deque
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass
class Player:
    score: int


@dataclass(frozen=True)
class Game:
    players: list[Player]
    board: deque[int]

    def play(self, moves: int) -> None:
        for i in range(moves):
            value = i + 1
            if value % 23 == 0:
                self.board.rotate(-6)
                player = self.players[i % len(self.players)]
                player.score += value
                value = self.board.popleft()
                player.score += self.board.popleft()
            else:
                self.board.rotate(1)
            self.board.appendleft(value)

    def get_high_score(self) -> int:
        return max([player.score for player in self.players])


@answer.timer
def main() -> None:
    entries = Parser().entries()
    players, value = int(entries[0]), int(entries[-2])
    answer.part1(429943, solve(players, value))
    answer.part2(3615691746, solve(players, value * 100))


def solve(players: int, moves: int) -> int:
    game = Game(
        players=[Player(0) for _ in range(players)],
        board=deque([0]),
    )
    game.play(moves)
    return game.get_high_score()


if __name__ == "__main__":
    main()
