from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'
COMPARISON = 17, 61


class Entity:

    def __init__(self, to, value):
        self.to = to
        self.value = value

    def process(self, value, bots, outputs):
        if self.to == 'bot':
            bots[self.value].process(value, bots, outputs)
        elif self.to == 'output':
            outputs[self.value].append(value)
        else:
            raise Exception('Unknown type: {}'.format(self.to))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({} {})'.format(self.to, self.value)


class Bot:

    def __init__(self, id, low, high):
        self.id = id
        self.low = low
        self.high = high
        self.values = []

    def process(self, value, bots, outputs):
        self.values.append(value)
        if len(self.values) == 2:
            low = min(self.values)
            self.low.process(low, bots, outputs)

            high = max(self.values)
            self.high.process(high, bots, outputs)

            if low == COMPARISON[0] and high == COMPARISON[1]:
                print(self.id)

            self.values = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'low = {} high = {}'.format(self.low, self.high)


def main():
    initial_values, bots, outputs = get_data()
    # Part 1 = 118
    for bot, values in initial_values.items():
        for value in values:
            bots[bot].process(value, bots, outputs)
    # Part 2 = 143153
    print(multiply_outputs(outputs, [0, 1, 2]))


def multiply_outputs(outputs, buckets):
    result = 1
    for bucket in buckets:
        result *= outputs[bucket][0]
    return result

def get_data():
    initial_values, bots, outputs = defaultdict(list), {}, defaultdict(list)
    for line in Parser(FILE_NAME).lines():
        parts = line.split()

        if parts[0] == 'value':
            initial_values[int(parts[5])].append(int(parts[1]))

        if parts[0] == 'bot':
            bots[int(parts[1])] = Bot(
                int(parts[1]),
                Entity(parts[5], int(parts[6])), 
                Entity(parts[10], int(parts[11]))
            )

    return initial_values, bots, outputs


if __name__ == '__main__':
    main()

