from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    @staticmethod
    def clockwise(direction: "Direction") -> "Direction":
        if direction == Direction.UP:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.LEFT
        elif direction == Direction.LEFT:
            return Direction.UP

    @staticmethod
    def counter_clockwise(direction: "Direction") -> "Direction":
        if direction == Direction.UP:
            return Direction.LEFT
        elif direction == Direction.LEFT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.UP

    @staticmethod
    def from_str(s: str) -> "Direction":
        if s in ["^", "U"]:
            return Direction.UP
        elif s in ["v", "D"]:
            return Direction.DOWN
        elif s in ["<", "L"]:
            return Direction.LEFT
        elif s in [">", "R"]:
            return Direction.RIGHT
        else:
            raise Exception(f"Unknown direction: {s}")


type Point = tuple[int, int]


class PointHelper:
    @staticmethod
    def add(p1: Point, p2: Point) -> Point:
        return (p1[0] + p2[0], p1[1] + p2[1])

    @staticmethod
    def multiply(p: Point, amount: int) -> Point:
        return (p[0] * amount, p[1] * amount)

    @staticmethod
    def go(p: Point, direction: Direction) -> Point:
        if direction == Direction.UP:
            return (p[0], p[1] + 1)
        elif direction == Direction.DOWN:
            return (p[0], p[1] - 1)
        elif direction == Direction.LEFT:
            return (p[0] - 1, p[1])
        elif direction == Direction.RIGHT:
            return (p[0] + 1, p[1])

    @staticmethod
    def rotate(p: Point) -> Point:
        return (-p[1], p[0])

    @staticmethod
    def reflect(p: Point) -> Point:
        return (-p[0], p[1])

    @staticmethod
    def mirror(p: Point) -> Point:
        return (p[0], -p[1])

    @staticmethod
    def neighbors(p: Point) -> list[Point]:
        return [
            (p[0], p[1] + 1),
            (p[0], p[1] - 1),
            (p[0] + 1, p[1]),
            (p[0] - 1, p[1]),
        ]

    @staticmethod
    def neighbors_diagonal(p: Point) -> list[Point]:
        return [
            (p[0], p[1] + 1),
            (p[0], p[1] - 1),
            (p[0] + 1, p[1]),
            (p[0] - 1, p[1]),
            (p[0] - 1, p[1] - 1),
            (p[0] + 1, p[1] - 1),
            (p[0] - 1, p[1] + 1),
            (p[0] + 1, p[1] + 1),
        ]

    @staticmethod
    def distance(p1: Point, p2: Point) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def len(p: Point) -> int:
        return abs(p[0]) + abs(p[1])
