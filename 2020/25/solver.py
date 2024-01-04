from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Transformer:
    subject: int

    def get_loop_size(self, goal: int) -> int:
        loop_size: int = 0
        value: int = 1
        while value != goal:
            loop_size += 1
            value = self.next_value(value)
        return loop_size

    def run_loop(self, loop_size: int) -> int:
        value: int = 1
        for _ in range(loop_size):
            value = self.next_value(value)
        return value

    def next_value(self, value: int) -> int:
        return (value * self.subject) % 20201227


@answer.timer
def main() -> None:
    card, door = Parser().int_lines()
    loop_size = Transformer(7).get_loop_size(card)
    answer.part1(3015200, Transformer(door).run_loop(loop_size))


if __name__ == "__main__":
    main()
