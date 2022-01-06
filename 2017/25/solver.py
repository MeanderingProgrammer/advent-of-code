from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


MOVEMENTS = {
    'left': Point(-1),
    'right': Point(1)
}


class Rule:

    def __init__(self, raw):
        self.write = int(self.get_last(raw[0]))
        self.move = MOVEMENTS[self.get_last(raw[1])]
        self.next_state = self.get_last(raw[2])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {}, {})'.format(self.write, self.move, self.next_state)

    @staticmethod
    def get_last(raw):
        return raw.split()[-1][:-1]


class ConditionalRule:

    def __init__(self, raw):
        self.conditions = {}
        for i in range(0, len(raw), 4):
            self.conditions[self.get_value(raw[i])] = Rule(raw[i+1:i+4])

    def get(self, value):
        return self.conditions[value]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.conditions)

    @staticmethod
    def get_value(raw):
        return int(raw.split()[-1][:-1])


class TuringMachine:

    def __init__(self, state, rules):
        self.state = state
        self.rules = rules

        self.pos = Point(0)
        self.tape = Grid()

    def step(self):
        value = self.tape[self.pos] or 0
        transition = self.rules[self.state].get(value)

        self.tape[self.pos] = transition.write
        self.pos += transition.move
        self.state = transition.next_state

    def checksum(self):
        return sum([value for point, value in self.tape.items()])


def main():
    state, rules = get_state_rules()
    machine = TuringMachine(state[0], rules)
    for i in range(state[1]):
        machine.step()
    answer.part1(3099, machine.checksum())


def get_state_rules():
    groups = Parser().line_groups()
    state = get_state(groups[0])
    rules = {}
    for group in groups[1:]:
        rules[get_name(group[0])] = ConditionalRule(group[1:])
    return state, rules


def get_state(raw):
    start = get_name(raw[0])
    steps = int(raw[1].split()[-2])
    return start, steps


def get_name(raw):
    return raw.split()[-1][:-1]


if __name__ == '__main__':
    main()
