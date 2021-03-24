from aoc_parser import Parser
from aoc_board import Grid, Point


FILE_NAME = 'data'


class Memory:

    def __init__(self, state):
        self.state = state

    def redistribute(self):
        new_state = [v for v in self.state]

        selection = list(range(len(new_state)))
        selection.sort(key=lambda index: (-new_state[index], index))

        index = selection[0]
        amount = new_state[index]
        new_state[index] = 0

        for i in range(amount):
            index = (index + 1) % len(new_state)
            new_state[index] += 1

        return Memory(new_state)

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.state)


def main():
    seen = set()
    memory = Memory([int(v) for v in Parser(FILE_NAME).read().split()])

    cycles = 0
    while memory not in seen:
        seen.add(memory)
        memory = memory.redistribute()
        cycles += 1

    # Part 1 = 7864
    print('Cycles completed = {}'.format(cycles))

    caused_repitition = memory

    memory = memory.redistribute()
    cycles = 1

    while memory != caused_repitition:
        memory = memory.redistribute()
        cycles += 1

    # Part 2 = 1695
    print('Repitition seen again = {}'.format(cycles))


if __name__ == '__main__':
    main()

