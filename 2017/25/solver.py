from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser

MOVEMENTS = {"left": Point(-1), "right": Point(1)}


class Rule:
    def __init__(self, raw: list[str]):
        self.write = int(self.get_last(raw[0]))
        self.move = MOVEMENTS[self.get_last(raw[1])]
        self.next_state = self.get_last(raw[2])

    @staticmethod
    def get_last(raw):
        return raw.split()[-1][:-1]


class ConditionalRule:
    def __init__(self, raw: list[str]):
        self.conditions = {}
        for i in range(0, len(raw), 4):
            self.conditions[self.get_value(raw[i])] = Rule(raw[i + 1 : i + 4])

    def get(self, value: int) -> Rule:
        return self.conditions[value]

    @staticmethod
    def get_value(raw: str) -> int:
        return int(raw.split()[-1][:-1])


class TuringMachine:
    def __init__(self, state: str, rules: dict[str, ConditionalRule]):
        self.state = state
        self.rules = rules

        self.pos = Point(0)
        self.tape = Grid()

    def step(self) -> None:
        value = self.tape[self.pos] or 0
        transition = self.rules[self.state].get(value)

        self.tape[self.pos] = transition.write
        self.pos += transition.move
        self.state = transition.next_state

    def checksum(self) -> int:
        return sum([value for _, value in self.tape.items()])


def main() -> None:
    state, rules = get_state_rules()
    machine = TuringMachine(state[0], rules)
    for _ in range(state[1]):
        machine.step()
    answer.part1(3099, machine.checksum())


def get_state_rules() -> tuple[tuple[str, int], dict[str, ConditionalRule]]:
    groups = Parser().line_groups()
    state = get_state(groups[0])
    rules = {}
    for group in groups[1:]:
        rules[get_name(group[0])] = ConditionalRule(group[1:])
    return state, rules


def get_state(raw) -> tuple[str, int]:
    start = get_name(raw[0])
    steps = int(raw[1].split()[-2])
    return start, steps


def get_name(raw: str) -> str:
    return raw.split()[-1][:-1]


if __name__ == "__main__":
    main()
