class Instruction:

    def __init__(self, parts):
        self.opcode = parts[0]
        self.first = parts[1]
        self.second = parts[2]
        self.target = parts[3]

    def halt(self):
        return self.opcode == 99

    def process(self, memory):
        first = memory.get(self.first)
        second = memory.get(self.second)
        if self.opcode == 1:
            result = first + second
        else:
            result = first * second
        memory.set(self.target, result)


class Memory:

    def __init__(self, commands):
        self.commands = [int(command) for command in commands.split(',')]
        self.index = 0

    def get(self, i):
        return self.commands[i]

    def set(self, i, value):
        self.commands[i] = value

    def has_next(self):
        return self.index < len(self.commands)

    def next(self):
        portion = self.commands[self.index:self.index+4]
        self.index += 4
        return Instruction(portion)


class Computer:

    def __init__(self, memory):
        self.memory = memory

    def set_state(self, v1, v2):
        self.memory.set(1, v1)
        self.memory.set(2, v2)

    def run(self):
        while self.memory.has_next():
            instruction = self.memory.next()
            if instruction.halt():
                break
            instruction.process(self.memory)


def main():
    result = set_memory_and_run(12, 2)
    # Part 1: 6627023
    print('Part 1: {}'.format(result))
    noun, verb = get_goal_pair()
    # Part 2: 4019
    print('Part 2: {}'.format((100 * noun) + verb))


def get_goal_pair():
    for noun in range(100):
        for verb in range(100):
            result = set_memory_and_run(noun, verb)
            if result == 19_690_720:
                return noun, verb


def set_memory_and_run(v1, v2):
    memory = get_memory()
    computer = Computer(memory)
    computer.set_state(v1, v2)
    computer.run()
    return memory.get(0)


def get_memory():
    with open('data.txt', 'r') as f:
        return Memory(f.read())


if __name__ == '__main__':
    main()
