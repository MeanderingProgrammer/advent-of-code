from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Instruction:
    name: str
    value: str

    def is_mask(self) -> bool:
        return self.name == "mask"

    def memory_address(self) -> int:
        return int(self.name[4:-1])


@dataclass
class Computer:
    version: int
    mask: str
    memory: dict[int, int]

    def run(self, instruction: Instruction) -> None:
        if instruction.is_mask():
            self.mask = instruction.value
        else:
            if self.version == 1:
                self.v1(instruction.memory_address(), int(instruction.value))
            elif self.version == 2:
                self.v2(instruction.memory_address(), int(instruction.value))

    def v1(self, memory_address: int, value: int) -> None:
        self.memory[memory_address] = self.mask_v1(self.binary(value))

    def mask_v1(self, value: str) -> int:
        masked_value: str = ""
        for i in range(len(value)):
            mask_bit = self.mask[i]
            masked_value += value[i] if mask_bit == "X" else mask_bit
        return int(masked_value, 2)

    def v2(self, memory_address: int, value: int) -> None:
        for memory_mask in self.masks_v2(self.binary(memory_address)):
            self.memory[int(memory_mask, 2)] = value

    def masks_v2(self, value: str) -> list[str]:
        memory_masks: list[str] = [""]
        for i in range(len(value)):
            mask_bit = self.mask[i]
            if mask_bit != "X":
                to_add = value[i] if mask_bit == "0" else "1"
                for i in range(len(memory_masks)):
                    memory_masks[i] += to_add
            else:
                with_zero: list[str] = []
                for i in range(len(memory_masks)):
                    with_zero.append(memory_masks[i] + "0")
                    memory_masks[i] += "1"
                memory_masks.extend(with_zero)
        return memory_masks

    def binary(self, value: int) -> str:
        return bin(value)[2:].zfill(len(self.mask))


def main() -> None:
    answer.part1(10035335144067, run_computer(1))
    answer.part2(3817372618036, run_computer(2))


def run_computer(version: int) -> int:
    computer = Computer(version=version, mask="X" * 36, memory=dict())
    for instruction in get_instructions():
        computer.run(instruction)
    return sum(computer.memory.values())


def get_instructions() -> list[Instruction]:
    def parse_instruction(line: str) -> Instruction:
        name, value = line.split(" = ")
        return Instruction(name=name, value=value)

    return list(map(parse_instruction, Parser().lines()))


if __name__ == "__main__":
    main()
