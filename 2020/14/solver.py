from aoc import answer
from aoc.parser import Parser

LENGTH = 36


class Computer:
    def __init__(self, version):
        self.version = version
        self.mask = "X" * LENGTH
        self.memory = {}

    def run(self, instruction):
        if instruction.is_mask():
            self.mask = instruction.value
        else:
            if self.version == 1:
                self.apply_v1(instruction.get_memory_address(), instruction.get_value())
            elif self.version == 2:
                self.apply_v2(instruction.get_memory_address(), instruction.get_value())

    def apply_v2(self, memory_address, value):
        memory_masks = self.get_memory_masks_v2(self.to_binary_string(memory_address))
        for memory_mask in memory_masks:
            address = int(memory_mask, 2)
            self.memory[address] = value

    def get_memory_masks_v2(self, value):
        memory_masks = [""]
        for i in range(len(value)):
            value_bit = value[i]
            mask_bit = self.mask[i]
            if mask_bit != "X":
                to_add = value_bit if mask_bit == "0" else "1"
                for i in range(len(memory_masks)):
                    memory_masks[i] += to_add
            else:
                to_extend = []
                for i in range(len(memory_masks)):
                    to_extend.append(memory_masks[i] + "0")
                    memory_masks[i] += "1"
                memory_masks.extend(to_extend)
        return memory_masks

    def apply_v1(self, memory_address, value):
        self.memory[memory_address] = self.apply_mask_v1(self.to_binary_string(value))

    def apply_mask_v1(self, value):
        masked_value = ""
        for i in range(len(value)):
            value_bit = value[i]
            mask_bit = self.mask[i]
            to_add = value_bit if mask_bit == "X" else mask_bit
            masked_value += to_add
        return int(masked_value, 2)

    def to_binary_string(self, value):
        binary = bin(value)[2:]
        zeroes_needed = LENGTH - len(binary)
        leading_zeroes = "0" * zeroes_needed
        return leading_zeroes + binary

    def get_total_memory(self):
        total = 0
        for address in self.memory:
            value = self.memory[address]
            total += value
        return total


class Instruction:
    def __init__(self, instruction):
        parts = instruction.split(" = ")
        self.name = parts[0]
        self.value = parts[1]

    def is_mask(self):
        return self.name == "mask"

    def get_memory_address(self):
        return int(self.name[4:-1])

    def get_value(self):
        return int(self.value)


def main():
    answer.part1(10035335144067, run_computer(1))
    answer.part2(3817372618036, run_computer(2))


def run_computer(version):
    computer = Computer(version)
    instructions = get_instructions()
    for instruction in instructions:
        computer.run(instruction)
    return computer.get_total_memory()


def get_instructions():
    return [Instruction(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
