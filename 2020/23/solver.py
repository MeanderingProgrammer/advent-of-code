from aoc import answer
from aoc.parser import Parser


class Cup:
    def __init__(self, value):
        self.value = value
        self.next_cup = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        next_cup = "X" if self.next_cup is None else "->"
        return "{}: {}".format(self.value, next_cup)


class Cups:
    def __init__(self):
        self.root = None
        self.end = None
        self.references = [None] * 1_000_000

        self.low = None
        self.high = None

    def add(self, value):
        if self.low is None or value < self.low:
            self.low = value

        if self.high is None or value > self.high:
            self.high = value

        new_cup = Cup(value)
        if self.root is None:
            self.root = new_cup
            self.end = self.root
        else:
            self.end.next_cup = new_cup
            self.end = self.end.next_cup

        self.references[value - 1] = new_cup

    def wrap(self):
        self.end.next_cup = self.root

    def move(self):
        in_aside, aside = self.set_aside()
        destination_value = self.get_next_destination(in_aside)
        self.add_aside(destination_value, aside)
        self.root = self.root.next_cup

    def set_aside(self):
        aside = self.root.next_cup

        self.root.next_cup = self.root.next_cup.next_cup.next_cup.next_cup

        in_aside = [aside.value, aside.next_cup.value, aside.next_cup.next_cup.value]

        aside.next_cup.next_cup.next_cup = None

        return in_aside, aside

    def get_next_destination(self, in_aside):
        destination = self.root.value - 1
        if destination < self.low:
            destination = self.high
        while destination in in_aside:
            destination -= 1
            if destination < self.low:
                destination = self.high
        return destination

    def add_aside(self, destination_value, aside):
        destination = self.get_value_cup(destination_value)
        aside.next_cup.next_cup.next_cup = destination.next_cup
        destination.next_cup = aside

    def get_value_cup(self, value):
        return self.references[value - 1]

    def __str__(self):
        result = []
        current = self.get_value_cup(1).next_cup

        while current.value != 1:
            result.append(str(current.value))
            current = current.next_cup

        return "".join(result)


def main():
    answer.part1("45798623", run(None, 100))
    answer.part2(235551949822, run(1_000_000, 10_000_000))


def run(num_cups, loops):
    cups = get_cups(num_cups)
    for i in range(loops):
        cups.move()

    if num_cups is None:
        return str(cups)
    else:
        cup_value_1 = cups.get_value_cup(1)
        next_to_1 = cup_value_1.next_cup.value
        next_to_next_to_1 = cup_value_1.next_cup.next_cup.value
        return next_to_1 * next_to_next_to_1


def get_cups(num_cups):
    cups = Cups()
    for value in Parser().string():
        cups.add(int(value))

    if num_cups is not None:
        for i in range(cups.high + 1, num_cups + 1):
            cups.add(i)

    cups.wrap()
    return cups


if __name__ == "__main__":
    main()
