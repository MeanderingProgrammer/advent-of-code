from aoc import answer
from aoc.parser import Parser


class Game:
    def __init__(self, value):
        self.value = value

    def play(self) -> None:
        result = [[1, self.value[0]]]
        for n in range(1, len(self.value)):
            previous = self.value[n - 1]
            current = self.value[n]
            if previous == current:
                result[-1][0] += 1
            else:
                result.append([1, current])

        self.value = []
        for part in result:
            self.value.append(str(part[0]))
            self.value.append(part[1])


def main() -> None:
    value = Parser(strip=True).string()
    game = Game(value)
    answer.part1(360154, run(game, 40))
    answer.part2(5103798, run(game, 10))


def run(game: Game, rounds: int) -> int:
    for _ in range(rounds):
        game.play()
    return len(game.value)


if __name__ == "__main__":
    main()
