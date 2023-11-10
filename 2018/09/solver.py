from collections import deque
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass
class Player:
    id: int
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


def main() -> None:
    values = Parser().entries()
    num_players, highest_value = int(values[0]), int(values[-2])
    answer.part1(429943, solve(num_players, highest_value))
    answer.part2(3615691746, solve(num_players, highest_value * 100))


def solve(num_players: int, num_moves: int) -> int:
    game = Game(
        players=[Player(i + 1, 0) for i in range(num_players)],
        board=deque([0]),
    )
    game.play(num_moves)
    return game.get_high_score()


if __name__ == "__main__":
    main()
