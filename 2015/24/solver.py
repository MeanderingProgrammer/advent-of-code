import itertools
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass
class Organizer:
    weights: list[int]

    def run(self, sections: int) -> int:
        target: int = sum(self.weights) // sections
        entaglements: list[int] = []
        for weights in self.combinations(target):
            entaglements.append(Organizer.product(weights))
        return min(entaglements)

    def combinations(self, target: int) -> list[list[int]]:
        k: int = 0
        result: list[list[int]] = []
        while len(result) == 0:
            k += 1
            for weights in itertools.combinations(self.weights, k):
                if sum(weights) == target:
                    result.append(list(weights))
        return result

    @staticmethod
    def product(weights: list[int]) -> int:
        result = 1
        for weight in weights:
            result *= weight
        return result


@answer.timer
def main() -> None:
    weights = Parser().int_lines()
    organizer = Organizer(weights)
    answer.part1(10439961859, organizer.run(3))
    answer.part2(72050269, organizer.run(4))


if __name__ == "__main__":
    main()
