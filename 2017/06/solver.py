from aoc import answer
from aoc.parser import Parser


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
    memory = Memory(Parser().int_entries())

    seen = set()

    def unique(memory):
        seen_before = memory in seen
        seen.add(memory)
        return not seen_before

    memory, cycles = run_as_long(memory, unique)

    answer.part1(7864, cycles)

    caused_repitition = memory

    def not_equal(memory):
        return memory != caused_repitition

    memory, cycles = run_as_long(memory.redistribute(), not_equal)

    answer.part2(1695, cycles + 1)


def run_as_long(memory, f):
    cycles = 0
    while f(memory):
        memory = memory.redistribute()
        cycles += 1
    return memory, cycles


if __name__ == "__main__":
    main()
