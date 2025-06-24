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


@dataclass(frozen=True)
class Instruction:
    op: str
    args: list[str]

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

    @staticmethod
    def new(line: str) -> "Instruction":
        op, args = line.split(" ", 1)
        return Instruction(op, args.split(", "))


@answer.timer
def main() -> None:
    instructions = [Instruction.new(line) for line in Parser().lines()]
    answer.part1(170, run(instructions, 0))
    answer.part2(247, run(instructions, 1))


def run(instructions: list[Instruction], a: int) -> int:
    computer = Computer(registers=dict(a=a, b=0))
    computer.run(instructions)
    return computer.get("b")


if __name__ == "__main__":
    main()
