from dataclasses import dataclass
from typing import Optional

from aoc import answer
from aoc.parser import Parser

BUFFER: int = 2


@dataclass(frozen=True)
class Rule:
    pattern: list[str]
    output: str

    def matches(self, values: list[str]) -> bool:
        return values == self.pattern


@dataclass
class State:
    state: dict[int, str]
    min: int
    max: int

    def apply_rules(self, rules: list[Rule]) -> None:
        changes: dict[int, str] = dict()
        for i in range(self.min - BUFFER, self.max + BUFFER + 1):
            rule = self.get_matching(rules, i)
            output = rule.output if rule is not None else "."
            if i < self.min:
                if output == "#":
                    changes[i] = output
                    self.min = i
            elif i > self.max:
                if output == "#":
                    changes[i] = output
                    self.max = i
            else:
                changes[i] = output
        for i, change in changes.items():
            self.state[i] = change

    def get_matching(self, rules: list[Rule], i: int) -> Optional[Rule]:
        for rule in rules:
            values = [
                self.state.get(index, ".")
                for index in range(i - BUFFER, i + BUFFER + 1)
            ]
            if rule.matches(values):
                return rule
        return None

    def value(self) -> int:
        return sum([i for i, value in self.state.items() if value == "#"])


def main() -> None:
    answer.part1(1816, run_for(20))
    answer.part2(399999999957, solve_known(50_000_000_000))


def run_for(generations: int) -> int:
    def parse_state(line: str) -> State:
        state: dict[int, str] = dict()
        values = line.split(": ")[1]
        for i, value in enumerate(values):
            state[i] = value
        return State(
            state=state,
            min=0,
            max=len(values) - 1,
        )

    def parse_rule(line: str) -> Rule:
        pattern, output = line.split(" => ")
        return Rule(
            pattern=list(pattern),
            output=output,
        )

    groups = Parser().line_groups()
    state = parse_state(groups[0][0])
    rules = [parse_rule(rule) for rule in groups[1]]
    for _ in range(generations):
        state.apply_rules(rules)
    return state.value()


def solve_known(generations: int) -> int:
    # Found a simple pattern after 156 generations by
    # printing value of state after each generation, not
    # sure if there is a more clever way to get there
    num_constant = generations - 156
    return (num_constant * 8) + 1_205


if __name__ == "__main__":
    main()
