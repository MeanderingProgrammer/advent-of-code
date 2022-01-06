import commons.answer as answer
from commons.aoc_parser import Parser
from commons.int_code import Computer
from commons.aoc_board import Point


STATE_MAPPING = {
    '^': 0,
    '>': 1,
    'v': 2,
    '<': 3
}

DIRECTIONS = [
    Point(0, -1),
    Point(1, 0),
    Point(0, 1),
    Point(-1, 0)
]


class DroidState:

    def __init__(self, location, scafolding, direction):
        self.location = location
        self.scafolding = scafolding
        self.direction = DIRECTIONS[STATE_MAPPING[direction]]

    def has_next(self):
        return self.get_direction() is not None

    def get_instruction(self):
        code, self.direction = self.get_direction()
        return code, self.move_until_end()

    def get_direction(self):
        direction_index = DIRECTIONS.index(self.direction)

        left = DIRECTIONS[direction_index - 1]
        right = DIRECTIONS[(direction_index + 1) % len(DIRECTIONS)]

        if (self.location + left) in self.scafolding:
            return 'L', left
        elif (self.location + right) in self.scafolding:
            return 'R', right
        else:
            return None

    def move_until_end(self):
        amount = 0
        while (self.location + self.direction) in self.scafolding:
            self.location += self.direction
            amount += 1
        return amount

    def __str__(self):
        return 'Location = {}\nPosition = {}'.format(self.location, self.direction)


class VacuumDroid:

    def __init__(self):
        self.__computer = Computer(self)

        self.__current = Point(0, 0)
        self.__state = None
        self.__scafolding = set()

        self.__instructions = []
        self.__index = 0
        self.running = False
        self.value = None

    def set_memory(self, memory):
        self.__computer.set_memory(memory)

    def run(self):
        self.__computer.run()

    def get_input(self):
        if self.__index >= len(self.__instructions):
            raise Exception('PASSED END')
        value = self.__instructions[self.__index]
        self.__index += 1
        return value

    def add_output(self, value):
        if self.running:
            self.value = value
            return
        value = chr(value)
        if value == '\n':
            self.__current = Point(0, self.__current.y() + 1)
        else:
            if value != '.':
                self.__scafolding.add(self.__current)
                if value != '#':
                    self.__state = DroidState(self.__current, self.__scafolding, value)
            self.__current = self.__current.right()

    def get_intersections(self):
        intersections = set()
        for point in self.__scafolding:
            contains = [adjacent in self.__scafolding for adjacent in point.adjacent()]
            if all(contains):
                intersections.add(point)
        return intersections

    def create_path(self):
        instructions = []
        while self.__state.has_next():
            instructions.append(self.__state.get_instruction())
        a, a_bounds, b, b_bounds, c, c_bounds = self.compress_instructions(instructions, 5)
        routine = self.create_routine(a_bounds, b_bounds, c_bounds, len(instructions))
        self.add_instruction(routine)
        self.add_instruction(a)
        self.add_instruction(b)
        self.add_instruction(c)
        self.__instructions.append(ord('n'))
        self.__instructions.append(10)

    def add_instruction(self, instructions):
        if type(instructions[0]) is str:
            instructions = ','.join(instructions)
        else:
            instructions = ','.join(['{},{}'.format(*instruction) for instruction in instructions])
        for ch in instructions:
            self.__instructions.append(ord(ch))
        self.__instructions.append(10)

    def create_routine(self, a_bounds, b_bounds, c_bounds, end):
        i = 0
        routine = []
        while i < end:
            a_end = self.get_end_bound(i, a_bounds)
            b_end = self.get_end_bound(i, b_bounds)
            c_end = self.get_end_bound(i, c_bounds)
            if a_end is not None:
                routine.append('A')
                i = a_end
            elif b_end is not None:
                routine.append('B')
                i = b_end
            elif c_end is not None:
                routine.append('C')
                i = c_end
            else:
                raise Exception('OOOPS')
        return routine

    def compress_instructions(self, instructions, max_length):
        total_instructions = len(instructions)
        for i in range(1, 1+max_length):
            a = instructions[:i]
            a_bounds = self.get_bounds(a, instructions)

            start_j = i
            while self.in_bounds(start_j, a_bounds):
                start_j += len(a)

            for j in range(1+start_j, 1+start_j+max_length):
                b = instructions[start_j:j]
                b_bounds = self.get_bounds(b, instructions)

                start_k = j
                while self.in_bounds(start_k, a_bounds) or self.in_bounds(start_k, b_bounds):
                    if self.in_bounds(start_k, a_bounds):
                        start_k += len(a)
                    else:
                        start_k += len(b)

                for k in range(1+start_k, 1+start_k+max_length):
                    c = instructions[start_k:k]
                    c_bounds = self.get_bounds(c, instructions)

                    all_bounds = [a_bounds, b_bounds, c_bounds]
                    total_bounds = sum([len(bound) for bound in all_bounds])
                    if self.contains_all(all_bounds, total_instructions):
                        return (a, a_bounds, b, b_bounds, c, c_bounds)

    def get_bounds(self, sublist, main):
        bounds = []
        i = 0
        while i < (len(main) - len(sublist)) + 1:
            contained = True
            for j in range(len(sublist)):
                if main[i+j] != sublist[j]:
                    contained = False
            if contained:
                bounds.append((i, i + len(sublist)))
            i += 1
        return bounds

    def contains_all(self, all_bounds, total_instructions):
        flattened = [bound for bounds in all_bounds for bound in bounds]
        for i in range(total_instructions):
            if not self.in_bounds(i, flattened):
                return False
        return True

    def in_bounds(self, index, bounds):
        for bound in bounds:
            if index >= bound[0] and index < bound[1]:
                return True
        return False

    def get_end_bound(self, index, bounds):
        for bound in bounds:
            if index == bound[0]:
                return bound[1]
        return None

    def __str__(self):
        return 'Scafolding = {}\nLocation = {}'.format(self.__scafolding, self.__state)


def main():
    droid = VacuumDroid()
    answer.part1(9876, total_alignment(droid))
    answer.part2(1234055, dust_collected(droid))


def total_alignment(droid):
    run_droid(droid, False)
    intersections = droid.get_intersections()
    alignments = [get_alignment(intersection) for intersection in intersections]
    return sum(alignments)


def get_alignment(point):
    return point.x() * point.y()


def dust_collected(droid):
    droid.create_path()
    droid.running = True
    run_droid(droid, True)
    return droid.value


def run_droid(droid, prompt):
    memory = get_memory()
    if prompt:
        # Set memory at address 0 to 2 to be prompted for input
        memory[0] = 2
    droid.set_memory(memory)
    droid.run()


def get_memory():
    return Parser().int_csv()


if __name__ == '__main__':
    main()
