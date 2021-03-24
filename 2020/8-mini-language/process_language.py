class Acc:

    def __init__(self, value):
        self.value = value

    def execute(self, instruction_set):
        #print('Acc', self.value)
        instruction_set.acc += self.value
        instruction_set.command += 1


class Jmp:

    def __init__(self, value):
        self.value = value

    def execute(self, instruction_set):
        #print('Jmp', self.value)
        instruction_set.command += self.value


class Nop:

    def __init__(self, value):
        self.value = value

    def execute(self, instruction_set):
        #print('Nop', self.value)
        instruction_set.command += 1


class InstructionSet:

    def __init__(self):
        self.instructions = []

        # Reset per execution of excute
        self.acc = 0
        self.command = 0
        self.seen = set()

    def add(self, instruction):
        parts = instruction.split()
        command = parts[0]
        value = self.get_value(parts[1])
        if command == 'acc':
            instruction = Acc(value)
        elif command == 'jmp':
            instruction = Jmp(value)
        elif command == 'nop':
            instruction = Nop(value)
        self.instructions.append(instruction)

    def attempt_to_fix(self):
        self.execute()
        commands_to_iterate = set(self.seen)
        for command in commands_to_iterate:
            instruction = self.instructions[command]
            if isinstance(instruction, Jmp):
                self.instructions[command] = Nop(instruction.value)
            elif isinstance(instruction, Nop):
                self.instructions[command] = Jmp(instruction.value)
            if self.execute():
                return self.acc
            self.instructions[command] = instruction


    def execute(self):
        self.acc = 0
        self.command = 0
        self.seen = set()
        return self.inner_execute()

    def inner_execute(self):
        if self.command in self.seen:
            return False

        self.seen.add(self.command)

        if len(self.instructions) == self.command:
            return True

        instruction = self.instructions[self.command]
        instruction.execute(self)

        return self.inner_execute()


    @staticmethod
    def get_value(value):
        sign = value[0]
        value = int(value[1:])
        if sign == '-':
            value *= -1
        return value


def main():
    instructions = get_instructions()
    acc = instructions.attempt_to_fix()
    print('Acc before fail = {}'.format(acc))


def get_instructions():
    instructions = InstructionSet()
    f = open('data.txt', 'r')

    for line in f:
        line = line.strip()
        instructions.add(line)

    f.close()
    return instructions


if __name__ == '__main__':
    main()

