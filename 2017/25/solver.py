from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser

MOVEMENTS: dict[str, int] = dict(left=-1, right=1)


class Rule:
    def __init__(self, raw: list[str]):
        self.write: int = int(Rule.get_last(raw[0]))
        self.move: int = MOVEMENTS[self.get_last(raw[1])]
        self.next_state: str = Rule.get_last(raw[2])

    @staticmethod
    def get_last(raw: str) -> str:
        return raw.split()[-1][:-1]


class Conditional:
    def __init__(self, raw: list[str]):
        self.conditions: dict[int, Rule] = {}
        for i in range(0, len(raw), 4):
            self.conditions[Conditional.get_value(raw[i])] = Rule(raw[i + 1 : i + 4])

    def get(self, value: int) -> Rule:
        return self.conditions[value]

    @staticmethod
    def get_value(raw: str) -> int:
        return int(raw.split()[-1][:-1])


@dataclass
class TuringMachine:
    state: str
    rules: dict[str, Conditional]
    pos: int
    tape: dict[int, int]

    def step(self) -> None:
        value = self.tape.get(self.pos, 0)
        transition = self.rules[self.state].get(value)

        self.tape[self.pos] = transition.write
        self.pos += transition.move
        self.state = transition.next_state

    def checksum(self) -> int:
        return sum([value for _, value in self.tape.items()])


@answer.timer
def main() -> None:
    groups = Parser().line_groups()
    state, rules = get_state_rules(groups)
    machine = TuringMachine(state[0], rules, 0, dict())
    for _ in range(state[1]):
        machine.step()
    answer.part1(3099, machine.checksum())


def get_state_rules(
    groups: list[list[str]],
) -> tuple[tuple[str, int], dict[str, Conditional]]:
    state = get_state(groups[0])
    rules: dict[str, Conditional] = dict()
    for group in groups[1:]:
        rules[get_name(group[0])] = Conditional(group[1:])
    return state, rules


def get_state(raw: list[str]) -> tuple[str, int]:
    start = get_name(raw[0])
    steps = int(raw[1].split()[-2])
    return start, steps


def get_name(raw: str) -> str:
    return raw.split()[-1][:-1]


if __name__ == "__main__":
    main()
