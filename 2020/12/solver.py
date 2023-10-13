from aoc import answer
from aoc.parser import Parser

COMMANDS_V1 = {
    "L": lambda point, pos, amount: (point.rotate_left(amount), pos),
    "N": lambda point, pos, amount: (point, pos + Position(0, amount)),
    "E": lambda point, pos, amount: (point, pos + Position(amount, 0)),
    "F": lambda point, pos, amount: (point, pos + point * amount),
}

COMMANDS_V2 = {
    "L": lambda point, pos, amount: (point.rotate_left(amount), pos),
    "N": lambda point, pos, amount: (point + Position(0, amount), pos),
    "E": lambda point, pos, amount: (point + Position(amount, 0), pos),
    "F": lambda point, pos, amount: (point, pos + point * amount),
}


class Ship:
    def __init__(self, commands, is_v1):
        self.commands = commands
        self.__point = Position(1, 0) if is_v1 else Position(10, 1)
        self.__pos = Position(0, 0)

    def move(self, instruction):
        self.__point, self.__pos = self.commands[instruction.get_command()](
            self.__point, self.__pos, instruction.get_amount()
        )

    def get_position(self):
        return self.__pos


class Position:
    def __init__(self, x, y):
        self.__x, self.__y = x, y

    def rotate_left(self, amount):
        x, y = self.__x, self.__y
        for i in range(amount // 90):
            x, y = y * -1, x
        return Position(x, y)

    def get_distance(self):
        return abs(self.x) + abs(self.y)

    def __add__(self, other):
        return Position(self.__x + other.__x, self.__y + other.__y)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, amount):
        return Position(self.__x * amount, self.__y * amount)

    def __rmul__(self, amount):
        return self.__mul__(amount)

    def __len__(self):
        return abs(self.__x) + abs(self.__y)


TRANSFORMS = {
    "R": lambda amount: ("L", 360 - amount),
    "S": lambda amount: ("N", amount * -1),
    "W": lambda amount: ("E", amount * -1),
}


class Instruction:
    def __init__(self, instruction):
        self.__command, self.__amount = instruction[0], int(instruction[1:])
        if self.__command in TRANSFORMS:
            self.__command, self.__amount = TRANSFORMS[self.__command](self.__amount)

    def get_command(self):
        return self.__command

    def get_amount(self):
        return self.__amount


def main():
    answer.part1(362, move_ship(True))
    answer.part2(29895, move_ship(False))


def move_ship(is_v1):
    commands = COMMANDS_V1 if is_v1 else COMMANDS_V2
    ship = Ship(commands, is_v1)
    for instruction in get_instructions():
        ship.move(instruction)
    return len(ship.get_position())


def get_instructions():
    return [Instruction(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
