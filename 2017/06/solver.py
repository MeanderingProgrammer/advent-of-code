from dataclasses import dataclass
from typing import Callable, Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Memory:
    state: tuple[int, ...]

    def redistribute(self) -> Self:
        new_state = [v for v in self.state]

        selection = list(range(len(new_state)))
        selection.sort(key=lambda index: (-new_state[index], index))

        index = selection[0]
        amount = new_state[index]
        new_state[index] = 0
        for _ in range(amount):
            index = (index + 1) % len(new_state)
            new_state[index] += 1

        return type(self)(tuple(new_state))


@answer.timer
def main() -> None:
    memory = Memory(tuple(Parser().int_entries()))
    seen: set[Memory] = set()

    def unique(memory: Memory) -> bool:
        seen_before = memory in seen
        seen.add(memory)
        return not seen_before

    memory, cycles = run_as_long(memory, unique)
    answer.part1(7864, cycles)

    caused_repitition = memory

    def not_equal(memory: Memory) -> bool:
        return memory != caused_repitition

    memory, cycles = run_as_long(memory.redistribute(), not_equal)
    answer.part2(1695, cycles + 1)


def run_as_long(memory: Memory, f: Callable[[Memory], bool]) -> tuple[Memory, int]:
    cycles = 0
    while f(memory):
        memory = memory.redistribute()
        cycles += 1
    return memory, cycles


if __name__ == "__main__":
    main()
