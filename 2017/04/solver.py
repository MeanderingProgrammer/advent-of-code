from collections import defaultdict
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Password:
    words: list[str]

    def valid(self, check_anagram: bool) -> bool:
        frequency = defaultdict(int)
        for word in self.words:
            word = Password.anagram(word) if check_anagram else word
            frequency[word] += 1
        return all([value == 1 for value in frequency.values()])

    @staticmethod
    def anagram(word: str) -> frozenset:
        anagram = defaultdict(int)
        for letter in word:
            anagram[letter] += 1
        return frozenset(anagram.items())


@answer.timer
def main() -> None:
    answer.part1(466, count_valid(False))
    answer.part2(251, count_valid(True))


def count_valid(check_anagram: bool) -> int:
    are_valid: list[bool] = []
    for line in Parser().lines():
        valid = Password(line.split()).valid(check_anagram)
        are_valid.append(valid)
    return sum(are_valid)


if __name__ == "__main__":
    main()
