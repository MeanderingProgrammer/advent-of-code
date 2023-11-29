from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser

CONTROLS: dict[str, Point] = dict(
    U=Point(0, -1),
    D=Point(0, 1),
    L=Point(-1, 0),
    R=Point(1, 0),
)


def main() -> None:
    answer.part1("47978", get_code([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    answer.part2(
        "659AD",
        get_code(
            [
                ["*", "*", 1, "*", "*"],
                ["*", 2, 3, 4, "*"],
                [5, 6, 7, 8, 9],
                ["*", "A", "B", "C", "*"],
                ["*", "*", "D", "*", "*"],
            ]
        ),
    )


def get_code(pattern: list[list[int | str]]) -> str:
    phone, position = create_phone(pattern)
    code = ""
    for instruction in Parser().lines():
        position = follow(phone, position, instruction)
        code += str(phone[position])
    return code


def create_phone(pattern: list[list[int | str]]) -> tuple[Grid, Point]:
    phone = Grid()
    start = None
    for y, row in enumerate(pattern):
        for x, value in enumerate(row):
            point = Point(x, y)
            if value != "*":
                phone[point] = value
            if value == 5:
                start = point
    assert start is not None
    return phone, start


def follow(phone: Grid, position: Point, instruction: str) -> Point:
    for direction in instruction:
        new_position = position + CONTROLS[direction]
        if new_position in phone:
            position = new_position
    return position


if __name__ == "__main__":
    main()
