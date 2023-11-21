from aoc import answer
from aoc.parser import Parser


class Cups:
    def __init__(self, values: list[int]):
        self.current: int = values[0]
        self.low: int = min(values)
        self.high: int = max(values)
        # Mapping from current cup to one immediately following it
        self.cups: dict[int, int] = dict(zip(values, values[1:] + [values[0]]))

    def move(self) -> None:
        aside = [self.cups[self.current]]
        aside.append(self.cups[aside[-1]])
        aside.append(self.cups[aside[-1]])
        destination = self.get_destination(aside)
        self.cups[self.current] = self.cups[aside[-1]]
        self.cups[aside[-1]] = self.cups[destination]
        self.cups[destination] = aside[0]
        self.current = self.cups[self.current]

    def get_destination(self, aside: list[int]) -> int:
        destination = self.previous(self.current)
        while destination in aside:
            destination = self.previous(destination)
        return destination

    def previous(self, value: int) -> int:
        value = value - 1
        if value < self.low:
            value = self.high
        return value

    def part_1(self) -> str:
        result = ""
        value = self.cups[1]
        while value != 1:
            result += str(value)
            value = self.cups[value]
        return result

    def part_2(self) -> int:
        return self.cups[1] * self.cups[self.cups[1]]


def main() -> None:
    answer.part1("45798623", run(0, 100).part_1())
    answer.part2(235551949822, run(1_000_000, 10_000_000).part_2())


def run(num_cups: int, loops: int) -> Cups:
    values: list[int] = Parser().int_string()
    values.extend(range(max(values) + 1, num_cups + 1))
    cups = Cups(values)
    for _ in range(loops):
        cups.move()
    return cups


if __name__ == "__main__":
    main()
