from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    @classmethod
    def new(cls, s: str) -> Direction:
        if s in ["^", "U", "north"]:
            return cls.UP
        elif s in ["v", "D", "south"]:
            return cls.DOWN
        elif s in ["<", "L", "west"]:
            return cls.LEFT
        elif s in [">", "R", "east"]:
            return cls.RIGHT
        else:
            raise Exception(f"Unknown direction: {s}")

    def left(self) -> Direction:
        match self:
            case self.UP:
                return self.LEFT
            case self.LEFT:
                return self.DOWN
            case self.DOWN:
                return self.RIGHT
            case self.RIGHT:
                return self.UP

    def right(self) -> Direction:
        match self:
            case self.UP:
                return self.RIGHT
            case self.RIGHT:
                return self.DOWN
            case self.DOWN:
                return self.LEFT
            case self.LEFT:
                return self.UP

    def opposite(self) -> Direction:
        match self:
            case self.UP:
                return self.DOWN
            case self.DOWN:
                return self.UP
            case self.LEFT:
                return self.RIGHT
            case self.RIGHT:
                return self.LEFT


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
    def all_neighbors(p: Point) -> list[Point]:
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
    def manhattan(p1: Point, p2: Point) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def len(p: Point) -> int:
        return abs(p[0]) + abs(p[1])
