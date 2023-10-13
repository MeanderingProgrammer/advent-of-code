from aoc import answer
from aoc.parser import Parser

RULE_LENGTH = 5
RULE_BUFFER = 2


class State:
    def __init__(self, value):
        self.state = {}

        value = value.split(": ")[1]
        for i, state in enumerate(value):
            self.state[i] = state

        self.min = 0
        self.max = len(value) - 1

    def apply_rules(self, rules):
        changes = {}
        for i in range(self.min - RULE_BUFFER, self.max + RULE_BUFFER + 1):
            rule = self.get_matching_rule(rules, i)
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

        self.apply(changes)

    def apply(self, changes):
        for i in changes:
            self.state[i] = changes[i]

    def get_matching_rule(self, rules, i):
        for rule in rules:
            values = [
                self.state.get(index, ".")
                for index in range(i - RULE_BUFFER, i + RULE_BUFFER + 1)
            ]
            if rule.matches(values):
                return rule
        return None

    def value(self):
        values = []
        for i in self.state:
            if self.state[i] == "#":
                values.append(i)
        return sum(values)

    def __repr__(self):
        return str(self)

    def __str__(self):
        indexes = [i for i in self.state]
        indexes.sort()
        values = [self.state[i] for i in indexes]
        return "".join(values)


class Rule:
    def __init__(self, value):
        parts = value.split(" => ")
        self.pattern = [value for value in parts[0]]
        self.output = parts[1]

    def matches(self, values):
        return values == self.pattern

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{} -> {}".format(self.pattern, self.output)


def main():
    answer.part1(1816, run_for(get(), 20))
    answer.part2(399999999957, solve_known(50_000_000_000))


def run_for(state_rules, generations):
    state, rules = state_rules
    for i in range(generations):
        state.apply_rules(rules)
    return state.value()


def solve_known(generations):
    # Found a simple pattern after 156 generations by
    # printing value of state after each generation, not
    # sure if there is a more clever way to get there
    num_constant = generations - 156
    return (num_constant * 8) + 1_205


def get():
    groups = Parser().line_groups()
    state = State(groups[0][0])
    rules = [Rule(rule) for rule in groups[1]]
    return state, rules


if __name__ == "__main__":
    main()
