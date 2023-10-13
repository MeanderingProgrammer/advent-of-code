from aoc import answer
from aoc.parser import Parser
from collections import defaultdict


class Entity:
    def __init__(self, to, value):
        self.to = to
        self.value = value

    def process(self, value, bots, outputs):
        if self.to == "bot":
            bots[self.value].process(value, bots, outputs)
        elif self.to == "output":
            outputs[self.value].append(value)
        else:
            raise Exception("Unknown type: {}".format(self.to))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "({} {})".format(self.to, self.value)


class Bot:
    def __init__(self, id, low, high):
        self.id = id
        self.low = low
        self.high = high
        self.values = []
        self.held = []

    def process(self, value, bots, outputs):
        self.values.append(value)
        self.held.append(value)

        if len(self.values) == 2:
            low = min(self.values)
            self.low.process(low, bots, outputs)

            high = max(self.values)
            self.high.process(high, bots, outputs)

            self.values = []

    def held_all_values(self, values):
        for value in values:
            if value not in self.held:
                return False
        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "low = {} high = {}".format(self.low, self.high)


def main():
    initial_values, bots, outputs = get_data()
    for bot, values in initial_values.items():
        for value in values:
            bots[bot].process(value, bots, outputs)

    answer.part1(118, get_bot(bots.values(), [17, 61]).id)
    answer.part2(143153, multiply_outputs(outputs, [0, 1, 2]))


def get_bot(bots, values):
    for bot in bots:
        if bot.held_all_values(values):
            return bot


def multiply_outputs(outputs, buckets):
    result = 1
    for bucket in buckets:
        result *= outputs[bucket][0]
    return result


def get_data():
    initial_values, bots, outputs = defaultdict(list), {}, defaultdict(list)
    for line in Parser().lines():
        parts = line.split()

        if parts[0] == "value":
            initial_values[int(parts[5])].append(int(parts[1]))

        if parts[0] == "bot":
            bots[int(parts[1])] = Bot(
                int(parts[1]),
                Entity(parts[5], int(parts[6])),
                Entity(parts[10], int(parts[11])),
            )

    return initial_values, bots, outputs


if __name__ == "__main__":
    main()
