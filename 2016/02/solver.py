from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point

DIRECTIONS: dict[str, Point] = dict(
    U=(0, -1),
    D=(0, 1),
    L=(-1, 0),
    R=(1, 0),
)


@answer.timer
def main() -> None:
    instructions: list[str] = Parser().lines()
    keypad_1: list[list[str]] = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]
    answer.part1("47978", get_code(instructions, keypad_1))
    keypad_2: list[list[str]] = [
        ["*", "*", "1", "*", "*"],
        ["*", "2", "3", "4", "*"],
        ["5", "6", "7", "8", "9"],
        ["*", "A", "B", "C", "*"],
        ["*", "*", "D", "*", "*"],
    ]
    answer.part2("659AD", get_code(instructions, keypad_2))


def get_code(instructions: list[str], keypad: list[list[str]]) -> str:
    phone = create_phone(keypad)
    position: Point = {digit: location for location, digit in phone.items()}["5"]

    code: list[str] = []
    for instruction in instructions:
        for direction in instruction:
            dx, dy = DIRECTIONS[direction]
            new_position: Point = (position[0] + dx, position[1] + dy)
            if new_position in phone:
                position = new_position
        code.append(phone[position])
    return "".join(code)


def create_phone(pattern: list[list[str]]) -> Grid[str]:
    phone: Grid[str] = dict()
    for y, row in enumerate(pattern):
        for x, value in enumerate(row):
            if value != "*":
                phone[(x, y)] = value
    return phone


if __name__ == "__main__":
    main()
