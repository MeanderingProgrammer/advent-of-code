import math
from collections import defaultdict
from dataclasses import dataclass, field

from aoc import answer
from aoc.parser import Parser

type Instruction = tuple[str, list[str]]


@dataclass
class Computer:
    instructions: list[Instruction]
    regs: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    ip: int = 0
    multiplies: int = 0

    def run(self) -> None:
        while self.ip >= 0 and self.ip < len(self.instructions):
            op, args = self.instructions[self.ip]
            if op == "set":
                self.regs[args[0]] = self.value(args[1])
                self.ip += 1
            elif op == "sub":
                self.regs[args[0]] -= self.value(args[1])
                self.ip += 1
            elif op == "mul":
                self.regs[args[0]] *= self.value(args[1])
                self.multiplies += 1
                self.ip += 1
            elif op == "jnz":
                if self.value(args[0]) != 0:
                    self.ip += self.value(args[1])
                else:
                    self.ip += 1
            else:
                raise Exception(f"Unknown operation: {op}")

    def value(self, arg: str) -> int:
        if arg in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            return self.regs[arg]
        else:
            return int(arg)


@answer.timer
def main() -> None:
    lines = Parser().lines()
    answer.part1(9409, run_computer(lines))
    answer.part2(913, count_non_primes(109_900, 126_900, 17))


def run_computer(lines: list[str]) -> int:
    def parse_instruction(line: str) -> Instruction:
        parts = line.split()
        return parts[0], parts[1:]

    instructions = [parse_instruction(line) for line in lines]
    computer = Computer(instructions)
    computer.run()
    return computer.multiplies


def count_non_primes(start: int, end: int, step: int) -> int:
    non_primes = 0
    for value in range(start, end + 1, step):
        if not is_prime(value):
            non_primes += 1
    return non_primes


def is_prime(value: int) -> bool:
    for i in range(2, math.floor(math.sqrt(value)) + 1):
        if value % i == 0:
            return False
    return True


if __name__ == "__main__":
    main()
