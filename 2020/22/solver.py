from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Deck:
    id: int
    cards: list[int]

    def empty(self) -> bool:
        return len(self) == 0

    def next(self) -> int:
        return self.cards.pop(0)

    def add(self, cards: list[int]) -> None:
        self.cards.extend(cards)

    def score(self) -> int:
        return sum([(len(self.cards) - i) * card for i, card in enumerate(self.cards)])

    def copy(self, n: int) -> Self:
        return type(self)(self.id, self.cards[:n])

    def __len__(self) -> int:
        return len(self.cards)


@dataclass(frozen=True)
class Game:
    deck1: Deck
    deck2: Deck
    recursive: bool
    states: set[str]

    def play(self) -> Deck:
        return self.deck1 if self.get_winner() == 1 else self.deck2

    def get_winner(self) -> int:
        while not self.deck1.empty() and not self.deck2.empty():
            if not self.update_state():
                return self.deck1.id
            card1 = self.deck1.next()
            card2 = self.deck2.next()
            if self.recursive and card1 <= len(self.deck1) and card2 <= len(self.deck2):
                winner = Game(
                    deck1=self.deck1.copy(card1),
                    deck2=self.deck2.copy(card2),
                    recursive=self.recursive,
                    states=set(),
                ).get_winner()
            else:
                winner = self.deck1.id if card1 > card2 else self.deck2.id
            if winner == 1:
                self.deck1.add([card1, card2])
            else:
                self.deck2.add([card2, card1])
        return self.deck2.id if self.deck1.empty() else self.deck1.id

    def update_state(self) -> bool:
        state = str(self.deck1.cards) + str(self.deck2.cards)
        if state in self.states:
            return False
        else:
            self.states.add(state)
            return True


@answer.timer
def main() -> None:
    groups = Parser().line_groups()
    answer.part1(32102, run(groups, False))
    answer.part2(34173, run(groups, True))


def run(groups: list[list[str]], recursive: bool) -> int:
    def parse_deck(id: int, lines: list[str]) -> Deck:
        return Deck(id=id, cards=list(map(int, lines[1:])))

    game = Game(
        deck1=parse_deck(1, groups[0]),
        deck2=parse_deck(2, groups[1]),
        recursive=recursive,
        states=set(),
    )
    winner = game.play()
    return winner.score()


if __name__ == "__main__":
    main()
