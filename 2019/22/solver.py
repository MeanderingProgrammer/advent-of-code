from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass
class Deck:
    n: int
    a: int = 1
    b: int = 0

    def deal_into_new(self) -> None:
        self.apply(-1, -1)

    def cut(self, n: int) -> None:
        self.apply(1, -n)

    def deal(self, n: int) -> None:
        self.apply(n, 0)

    def apply(self, la: int, lb: int) -> None:
        self.a = la * self.a
        self.b = la * self.b + lb

    def index_of(self, index: int, times: int) -> int:
        a = self.calc_a(times)
        b = self.calc_b(a)
        return (a * index + b) % self.n

    def get(self, index: int, times: int) -> int:
        a = self.calc_a(times)
        b = self.calc_b(a)
        return ((index - b) * self.inv(a)) % self.n

    def calc_a(self, times: int) -> int:
        return pow(self.a, times, self.n)

    def calc_b(self, a: int) -> int:
        return (self.b * (a - 1) * self.inv(self.a - 1)) % self.n

    def inv(self, a: int) -> int:
        return pow(a, self.n - 2, self.n)


DEAL = "deal with increment "
CUT = "cut "
NEW_STACK = "deal into new stack"


@dataclass(frozen=True)
class Processor:
    line: str

    def apply(self, deck: Deck) -> None:
        if self.line.startswith(DEAL):
            argument = int(self.line[len(DEAL) :])
            deck.deal(argument)
        elif self.line.startswith(CUT):
            argument = int(self.line[len(CUT) :])
            deck.cut(argument)
        elif self.line == NEW_STACK:
            deck.deal_into_new()
        else:
            raise Exception(f"Unknown processor = {self.line}")


@answer.timer
def main() -> None:
    # I have no idea how this one works, I definitely took it off the Reddits
    answer.part1(4684, process_deck(10_007).index_of(2019, 1))
    answer.part2(
        452290953297, process_deck(119_315_717_514_047).get(2020, 101_741_582_076_661)
    )


def process_deck(n: int) -> Deck:
    deck = Deck(n)
    processors = [Processor(line) for line in Parser().lines()]
    for processor in processors:
        processor.apply(deck)
    return deck


if __name__ == "__main__":
    main()
