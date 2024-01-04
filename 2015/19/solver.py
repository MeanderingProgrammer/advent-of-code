from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Rule:
    start: str
    end: str

    def replace(self, value: str) -> set[str]:
        results: set[str] = set()
        for index in find_all(value, self.start):
            results.add(self.replace_at(value, index))
        return results

    def replace_at(self, value: str, index: int) -> str:
        before, after = value[:index], value[index:]
        return before + after.replace(self.start, self.end, 1)


@answer.timer
def main() -> None:
    groups = Parser().line_groups()
    rules = get_rules(groups[0])
    molecule = groups[1][0]
    answer.part1(576, len(run(rules, molecule)))
    answer.part2(207, replacements_needed(molecule))


def get_rules(lines: list[str]) -> list[Rule]:
    def parse_rule(line: str) -> Rule:
        start, end = line.split(" => ")
        return Rule(start=start, end=end)

    return [parse_rule(line) for line in lines]


def run(rules: list[Rule], molecule: str) -> set[str]:
    results: set[str] = set()
    for rule in rules:
        results |= rule.replace(molecule)
    return results


def replacements_needed(molecule: str) -> int:
    # Solution by askalski
    # https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/
    elements = sum([letter.isupper() for letter in molecule])
    rn_count = len(find_all(molecule, "Rn"))
    ar_count = len(find_all(molecule, "Ar"))
    y_count = len(find_all(molecule, "Y"))
    return elements - rn_count - ar_count - (2 * y_count) - 1


def find_all(s: str, pattern: str) -> list[int]:
    indexes: list[int] = []
    current = 0
    while current < len(s):
        index = s.find(pattern, current)
        if index == -1:
            break
        indexes.append(index)
        current = index + 1
    return indexes


if __name__ == "__main__":
    main()
