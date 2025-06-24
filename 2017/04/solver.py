from collections import defaultdict

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    lines = Parser().lines()
    answer.part1(466, count(lines, False))
    answer.part2(251, count(lines, True))


def count(lines: list[str], anagram: bool) -> int:
    result: int = 0
    for line in lines:
        result += 1 if valid(line.split(), anagram) else 0
    return result


def valid(words: list[str], anagram: bool) -> bool:
    frequency: dict[str, int] = defaultdict(int)
    for word in words:
        word = "".join(sorted(word)) if anagram else word
        frequency[word] += 1
    return all([value == 1 for value in frequency.values()])


if __name__ == "__main__":
    main()
