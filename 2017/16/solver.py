from collections import deque
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass
class Dance:
    dancers: deque[str]

    def spin(self, n: int) -> None:
        self.dancers.rotate(n)

    def exchange(self, i1: int, i2: int) -> None:
        temp = self.dancers[i1]
        self.dancers[i1] = self.dancers[i2]
        self.dancers[i2] = temp

    def partner(self, p1: str, p2: str) -> None:
        i1 = self.dancers.index(p1)
        i2 = self.dancers.index(p2)
        self.exchange(i1, i2)

    def __str__(self) -> str:
        return "".join(self.dancers)


@answer.timer
def main() -> None:
    moves: list[str] = Parser().csv()
    pattern = get_pattern(moves)
    answer.part1("eojfmbpkldghncia", pattern[1])
    answer.part2("iecopnahgdflmkjb", pattern[1_000_000_000 % len(pattern)])


def get_pattern(moves: list[str]) -> list[str]:
    dance: Dance = Dance(
        dancers=deque([chr(ord("a") + i) for i in range(16)]),
    )
    # Pattern happens to repeat from start immediately once we see
    # a value that is the same
    pattern: list[str] = []
    while str(dance) not in pattern:
        pattern.append(str(dance))
        perform_dance(dance, moves)
    return pattern


def perform_dance(dance: Dance, moves: list[str]) -> None:
    for move in moves:
        op, args = move[0], move[1:]
        if op == "s":
            dance.spin(int(args))
        elif op == "x":
            i1, i2 = args.split("/")
            dance.exchange(int(i1), int(i2))
        elif op == "p":
            p1, p2 = args.split("/")
            dance.partner(p1, p2)
        else:
            raise Exception(f"Unkown operation: {op}")


if __name__ == "__main__":
    main()
