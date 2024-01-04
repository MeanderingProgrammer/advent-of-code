from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class LetterRule:
    letter: str

    def matches(self, _: dict, value: str, index: int) -> set[int]:
        if index < len(value) and value[index] == self.letter:
            return set([index + 1])
        else:
            return set()


@dataclass(frozen=True)
class AndRule:
    rules: list[int]

    def matches(self, rules: dict, value: str, index: int) -> set[int]:
        result: set[int] = set([index])
        for rule in self.rules:
            new_matches = set()
            for match_index in result:
                new_matches.update(rules[rule].matches(rules, value, match_index))
            result = new_matches
        return result


@dataclass(frozen=True)
class OrRule:
    rules: list[AndRule]

    def matches(self, rules: dict, value: str, index: int) -> set[int]:
        result: set[int] = set()
        for rule in self.rules:
            result.update(rule.matches(rules, value, index))
        return result


@dataclass(frozen=True)
class Rules:
    rules: dict[int, LetterRule | OrRule | AndRule]

    def does_match(self, value: str) -> bool:
        return len(value) in self.rules[0].matches(self.rules, value, 0)


@answer.timer
def main() -> None:
    answer.part1(198, total_matches(False))
    answer.part2(372, total_matches(True))


def total_matches(part2: bool) -> int:
    groups = Parser().line_groups()
    rules = get_rules(groups[0], part2)
    return sum([rules.does_match(message) for message in groups[1]])


def get_rules(lines: list[str], part2: bool) -> Rules:
    def parse_and_rule(rules: str) -> AndRule:
        return AndRule(rules=list(map(int, rules.split(" "))))

    def parse_or_rule(rules: str) -> OrRule:
        return OrRule(rules=[parse_and_rule(rule) for rule in rules.split(" | ")])

    rules: dict[int, LetterRule | OrRule | AndRule] = dict()
    for line in lines:
        number, rule = line.split(": ")
        if rule.startswith('"') and rule.endswith('"'):
            rule = LetterRule(letter=rule[1])
        elif "|" in rule:
            rule = parse_or_rule(rule)
        else:
            rule = parse_and_rule(rule)
        rules[int(number)] = rule

    if part2:
        rules[8] = parse_or_rule("42 | 42 8")
        rules[11] = parse_or_rule("42 31 | 42 11 31")

    return Rules(rules=rules)


if __name__ == "__main__":
    main()
