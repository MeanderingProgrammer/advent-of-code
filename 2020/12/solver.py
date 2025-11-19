from dataclasses import dataclass
from typing import Callable, Self

from aoc import answer
from aoc.parser import Parser

type Command = Callable[[Position, Position, int], tuple[Position, Position]]

PART1: dict[str, Command] = {
    "L": lambda point, pos, amount: (point.rotate_left(amount), pos),
    "N": lambda point, pos, amount: (point, pos + Position(0, amount)),
    "E": lambda point, pos, amount: (point, pos + Position(amount, 0)),
    "F": lambda point, pos, amount: (point, pos + point * amount),
}

PART2: dict[str, Command] = {
    "L": lambda point, pos, amount: (point.rotate_left(amount), pos),
    "N": lambda point, pos, amount: (point + Position(0, amount), pos),
    "E": lambda point, pos, amount: (point + Position(amount, 0), pos),
    "F": lambda point, pos, amount: (point, pos + point * amount),
}


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def rotate_left(self, amount: int) -> Self:
        x, y = self.x, self.y
        for _ in range(amount // 90):
            x, y = y * -1, x
        return type(self)(x, y)

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Self) -> Self:
        return self.__add__(other)

    def __mul__(self, amount: int) -> Self:
        return type(self)(self.x * amount, self.y * amount)

    def __rmul__(self, amount: int) -> Self:
        return self.__mul__(amount)


@dataclass(frozen=True)
class Instruction:
    command: str
    amount: int

    @classmethod
    def new(cls, s: str) -> Self:
        command, amount = s[0], int(s[1:])
        if command == "R":
            return cls("L", 360 - amount)
        elif command == "S":
            return cls("N", amount * -1)
        elif command == "W":
            return cls("E", amount * -1)
        else:
            return cls(command, amount)


@dataclass
class Ship:
    commands: dict[str, Command]
    point: Position
    position: Position

    def move(self, instruction: Instruction) -> None:
        command = self.commands[instruction.command]
        self.point, self.position = command(
            self.point, self.position, instruction.amount
        )


@answer.timer
def main() -> None:
    instructions = [Instruction.new(line) for line in Parser().lines()]
    answer.part1(362, move_ship(instructions, True))
    answer.part2(29895, move_ship(instructions, False))


def move_ship(instructions: list[Instruction], part1: bool) -> int:
    ship = Ship(
        commands=PART1 if part1 else PART2,
        point=Position(1, 0) if part1 else Position(10, 1),
        position=Position(0, 0),
    )
    for instruction in instructions:
        ship.move(instruction)
    return abs(ship.position.x) + abs(ship.position.y)


if __name__ == "__main__":
    main()
