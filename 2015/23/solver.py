from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Computer:
    registers: dict[str, int]

    def get(self, register: str) -> int:
        return self.registers[register]

    def set(self, register: str, value: int) -> None:
        self.registers[register] = value

    def run(self, instructions: list["Instruction"]) -> None:
        ip = 0
        while ip >= 0 and ip < len(instructions):
            instruction = instructions[ip]
            move = instruction.run(self)
            ip += move


class Instruction:
    def __init__(self, raw):
        self.op, args = raw.split(" ", 1)
        self.args = [arg for arg in args.split(", ")]

    def run(self, computer: Computer) -> int:
        if self.op == "hlf":
            current = computer.get(self.args[0])
            computer.set(self.args[0], current // 2)
            return 1
        elif self.op == "tpl":
            current = computer.get(self.args[0])
            computer.set(self.args[0], current * 3)
            return 1
        elif self.op == "inc":
            current = computer.get(self.args[0])
            computer.set(self.args[0], current + 1)
            return 1
        elif self.op == "jmp":
            return int(self.args[0])
        elif self.op == "jie":
            current = computer.get(self.args[0])
            amount = int(self.args[1])
            return amount if current % 2 == 0 else 1
        elif self.op == "jio":
            current = computer.get(self.args[0])
            amount = int(self.args[1])
            return amount if current == 1 else 1
        else:
            raise Exception(f"Unknown operation: {self.op}")


def main() -> None:
    answer.part1(170, run_computer(0))
    answer.part2(247, run_computer(1))


def run_computer(a_value: int) -> int:
    computer = Computer(registers=dict(a=a_value, b=0))
    instructions = [Instruction(line) for line in Parser().lines()]
    computer.run(instructions)
    return computer.get("b")


if __name__ == "__main__":
    main()
