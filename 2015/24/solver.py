import itertools
from dataclasses import dataclass
from typing import Generator

from aoc import answer
from aoc.parser import Parser


@dataclass
class Organizer:
    weights: list[int]

    def run(self, sections: int) -> int:
        target = sum(self.weights) // sections
        groups_generator = Organizer.group(self.weights, target, sections)
        options = []
        for groups in groups_generator:
            if len(options) > 0 and len(groups[0]) > len(options[0]):
                break
            options.append(groups[0])
        return min([Organizer.entaglement(option) for option in options])

    @staticmethod
    def group(
        weights: list[int], target: int, section: int
    ) -> Generator[list[tuple[int, ...]], None, None]:
        for packages in range(1, len(weights) + 1):
            for sub_weights in itertools.combinations(weights, packages):
                if sum(sub_weights) != target:
                    continue
                if section == 1:
                    yield [sub_weights]
                remaining = [weight for weight in weights if weight not in sub_weights]
                for sub_groups in Organizer.group(remaining, target, section - 1):
                    yield [sub_weights] + sub_groups
                    # No need to search for multiple matches that start with
                    # the current sub group, simply continue to next group
                    break

    @staticmethod
    def entaglement(values: tuple[int]) -> int:
        result = 1
        for value in values:
            result *= value
        return result


def main() -> None:
    organizer = Organizer(weights=Parser().int_lines())
    answer.part1(10439961859, organizer.run(3))
    answer.part2(72050269, organizer.run(4))


if __name__ == "__main__":
    main()
