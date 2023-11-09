from collections import defaultdict
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Word:
    value: str

    @property
    def groups(self) -> list[str]:
        groups = []
        for i in range(len(self.value) - 1):
            groups.append(self.value[i] + self.value[i + 1])
        return groups

    def nice_1(self) -> bool:
        return (
            self.num_vowels() >= 3
            and self.contains_repeat()
            and not self.contains_illegal()
        )

    def num_vowels(self) -> int:
        vowels = ["a", "e", "i", "o", "u"]
        return sum([letter in vowels for letter in self.value])

    def contains_repeat(self) -> bool:
        for group in self.groups:
            if group[0] == group[1]:
                return True
        return False

    def contains_illegal(self) -> bool:
        groups = self.groups
        illegal_groups = ["ab", "cd", "pq", "xy"]
        for illegal_group in illegal_groups:
            if illegal_group in groups:
                return True
        return False

    def nice_2(self) -> bool:
        return self.repeat_non_overlapping() and self.creates_tripple()

    def repeat_non_overlapping(self) -> bool:
        groups = self.groups
        group_frequencies = defaultdict(int)
        group_frequencies[groups[0]] += 1
        for i, group in enumerate(groups[1:]):
            num_needed = 1 if group != groups[i] else 2
            if group_frequencies[group] >= num_needed:
                return True
            group_frequencies[group] += 1
        return False

    def creates_tripple(self) -> bool:
        groups = self.groups
        for i, group in enumerate(groups[1:]):
            if groups[i][0] == group[1]:
                return True
        return False


def main() -> None:
    words = [Word(line) for line in Parser().lines()]
    answer.part1(238, total_nice_words(words, False))
    answer.part2(69, total_nice_words(words, True))


def total_nice_words(words: list[Word], new_rules: bool) -> int:
    nice_words = []
    for word in words:
        is_nice = word.nice_2() if new_rules else word.nice_1()
        nice_words.append(is_nice)
    return sum(nice_words)


if __name__ == "__main__":
    main()
