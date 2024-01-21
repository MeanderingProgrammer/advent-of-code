from typing import Optional

from aoc import answer
from aoc.parser import Parser


class PasswordGenerator:
    def __init__(self, starting_value: str):
        self.value: list[int] = [
            PasswordGenerator.to_index(ch) for ch in starting_value
        ]

    def next(self) -> None:
        index = self.get_last_index_under(25)
        if index is not None:
            self.value[index] += 1
        else:
            index = 0
            self.value = [0] + self.value
        for i in range(index + 1, len(self.value)):
            self.value[i] = 0

    def get_last_index_under(self, n: int) -> Optional[int]:
        for i in range(len(self.value) - 1, -1, -1):
            if self.value[i] < n:
                return i
        return None

    def valid(self) -> bool:
        if not self.contains_triple():
            return False
        if self.contains_invalid():
            return False
        if not self.contains_pairs():
            return False
        return True

    def contains_triple(self) -> bool:
        for i in range(len(self.value) - 2):
            first, second, third = self.value[i], self.value[i + 1], self.value[i + 2]
            if first + 1 == second and second + 1 == third:
                return True
        return False

    def contains_invalid(self) -> bool:
        all_invalid: list[int] = [
            self.to_index("i"),
            self.to_index("o"),
            self.to_index("l"),
        ]
        for invalid in all_invalid:
            if invalid in self.value:
                return True
        return False

    def contains_pairs(self) -> bool:
        pairs: set[int] = set()
        for i, character in enumerate(self.value[:-1]):
            if character == self.value[i + 1]:
                pairs.add(character)
        return len(pairs) > 1

    def get_value(self) -> str:
        return "".join([chr(i + ord("a")) for i in self.value])

    @staticmethod
    def to_index(character: str) -> int:
        return ord(character) - ord("a")


@answer.timer
def main() -> None:
    value = Parser().string()
    generator = PasswordGenerator(value)
    answer.part1("hxbxxyzz", run(generator))
    answer.part2("hxcaabcc", run(generator))


def run(generator: PasswordGenerator) -> str:
    generator.next()
    while not generator.valid():
        generator.next()
    return generator.get_value()


if __name__ == "__main__":
    main()
