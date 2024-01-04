from collections import defaultdict

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    answer.part1("liwvqppc", error_correct_message(-1))
    answer.part2("caqfbzlh", error_correct_message(0))


def error_correct_message(n: int) -> str:
    words: list[str] = Parser().lines()
    frequencies: list[dict[str, int]] = [defaultdict(int) for _ in range(len(words[0]))]
    for word in words:
        for i, letter in enumerate(word):
            frequencies[i][letter] += 1
    message = [nth_most_common(frequency, n) for frequency in frequencies]
    return "".join(message)


def nth_most_common(frequency: dict[str, int], n: int) -> str:
    items: list[tuple[int, str]] = [
        (frequency, letter) for letter, frequency in frequency.items()
    ]
    items.sort()
    return items[n][1]


if __name__ == "__main__":
    main()
