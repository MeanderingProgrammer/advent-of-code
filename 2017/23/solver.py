from collections import defaultdict

from aoc import answer
from aoc.parser import Parser


class Computer:
    def __init__(self, instructions):
        self.regs = defaultdict(int)
        self.instructions = instructions
        self.ip = 0
        self.multiplies = 0

    def run(self) -> None:
        while self.ip >= 0 and self.ip < len(self.instructions):
            instruction = self.instructions[self.ip]
            self.ip += instruction.run(self)

    def value(self, arg: str) -> int:
        try:
            return int(arg)
        except ValueError:
            return self.regs[arg]


class Intstruction:
    def __init__(self, value: str):
        parts = value.split()
        self.op = parts[0]
        self.args = parts[1:]

    def run(self, computer: Computer) -> int:
        if self.op == "set":
            computer.regs[self.args[0]] = computer.value(self.args[1])
            return 1
        elif self.op == "sub":
            computer.regs[self.args[0]] -= computer.value(self.args[1])
            return 1
        elif self.op == "mul":
            computer.regs[self.args[0]] *= computer.value(self.args[1])
            computer.multiplies += 1
            return 1
        elif self.op == "jnz":
            if computer.value(self.args[0]) != 0:
                return computer.value(self.args[1])
            else:
                return 1
        else:
            raise Exception(f"Unknown operation: {self.op}")


@answer.timer
def main() -> None:
    answer.part1(9409, run_computer())
    answer.part2(913, count_non_primes(109_900, 126_900, 17))


def run_computer() -> int:
    instructions = [Intstruction(line) for line in Parser().lines()]
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
    for i in range(2, value):
        if value % i == 0:
            return False
    return True


if __name__ == "__main__":
    main()
