from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass()
class Generator:
    value: list[int]

    @classmethod
    def new(cls, s: str) -> Self:
        return cls([Generator.to_index(ch) for ch in s])

    def next(self) -> None:
        index = self.get_last_index_under(25)
        if index is None:
            self.value = [0] + self.value
            index = 0
        else:
            self.value[index] += 1
        for i in range(index + 1, len(self.value)):
            self.value[i] = 0

    def get_last_index_under(self, n: int) -> int | None:
        for i in range(len(self.value) - 1, -1, -1):
            if self.value[i] < n:
                return i
        return None

    def valid(self) -> bool:
        return (
            self.contains_triple()
            and not self.contains_invalid()
            and self.num_pairs() > 1
        )

    def contains_triple(self) -> bool:
        for i in range(len(self.value) - 2):
            start = self.value[i]
            if start + 1 == self.value[i + 1] and start + 2 == self.value[i + 2]:
                return True
        return False

    def contains_invalid(self) -> bool:
        all_invalid: list[int] = [
            Generator.to_index("i"),
            Generator.to_index("o"),
            Generator.to_index("l"),
        ]
        for invalid in all_invalid:
            if invalid in self.value:
                return True
        return False

    def num_pairs(self) -> int:
        pairs: set[int] = set()
        for i, character in enumerate(self.value[:-1]):
            if character == self.value[i + 1]:
                pairs.add(character)
        return len(pairs)

    def get_value(self) -> str:
        return "".join([chr(i + ord("a")) for i in self.value])

    @staticmethod
    def to_index(character: str) -> int:
        return ord(character) - ord("a")


@answer.timer
def main() -> None:
    value = Parser().string()
    generator = Generator.new(value)
    answer.part1("hxbxxyzz", run(generator))
    answer.part2("hxcaabcc", run(generator))


def run(generator: Generator) -> str:
    generator.next()
    while not generator.valid():
        generator.next()
    return generator.get_value()


if __name__ == "__main__":
    main()
