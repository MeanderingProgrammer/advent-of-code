from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Self


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

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


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def reflect(self) -> Self:
        return type(self)(-self.x, self.y)

    def rotate(self) -> Self:
        return type(self)(-self.y, self.x)

    def mirror(self) -> Self:
        return type(self)(self.x, -self.y)

    def neighbors(self) -> list[Self]:
        return [
            type(self)(self.x, self.y + 1),
            type(self)(self.x, self.y - 1),
            type(self)(self.x + 1, self.y),
            type(self)(self.x - 1, self.y),
        ]

    def neighbors_diagonal(self) -> list[Self]:
        return [
            type(self)(self.x, self.y + 1),
            type(self)(self.x, self.y - 1),
            type(self)(self.x + 1, self.y),
            type(self)(self.x - 1, self.y),
            type(self)(self.x - 1, self.y - 1),
            type(self)(self.x + 1, self.y - 1),
            type(self)(self.x - 1, self.y + 1),
            type(self)(self.x + 1, self.y + 1),
        ]

    def go(self, direction: Direction) -> Self:
        if direction == Direction.UP:
            return type(self)(self.x, self.y + 1)
        elif direction == Direction.DOWN:
            return type(self)(self.x, self.y - 1)
        elif direction == Direction.LEFT:
            return type(self)(self.x - 1, self.y)
        elif direction == Direction.RIGHT:
            return type(self)(self.x + 1, self.y)
        else:
            raise Exception(f"Unknown direction: {direction}")

    def __len__(self) -> int:
        return abs(self.x) + abs(self.y)

    def __add__(self, o: Self) -> Self:
        return type(self)(self.x + o.x, self.y + o.y)

    def __sub__(self, o: Self) -> Self:
        return type(self)(self.x - o.x, self.y - o.y)

    def __mul__(self, amount: int) -> Self:
        return type(self)(self.x * amount, self.y * amount)

    def __rmul__(self, amount: int) -> Self:
        return self.__mul__(amount)

    def __lt__(self, o: Self) -> bool:
        return (self.y, self.x) < (o.y, o.x)

    def __le__(self, o: Self) -> bool:
        return (self.y, self.x) <= (o.y, o.x)


@dataclass(frozen=True)
class Point3d:
    x: int
    y: int
    z: int

    def __len__(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __add__(self, o: Self) -> Self:
        return type(self)(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o: Self) -> Self:
        return type(self)(self.x - o.x, self.y - o.y, self.z - o.z)

    def __mul__(self, amount: int) -> Self:
        return type(self)(self.x * amount, self.y * amount, self.z * amount)

    def __rmul__(self, amount: int) -> Self:
        return self.__mul__(amount)

    def __lt__(self, o: Self) -> bool:
        return (self.z, self.y, self.x) < (o.z, o.y, o.x)

    def __le__(self, o: Self) -> bool:
        return (self.z, self.y, self.x) <= (o.z, o.y, o.x)


class Grid[T]:
    def __init__(self, grid: Optional[dict[Point, T]] = None):
        self.grid: dict[Point, T] = grid if grid is not None else dict()

    def get(self, point: Point, default_value: T) -> T:
        return self.grid.get(point, default_value)

    def items(self):
        return self.grid.items()

    def reflect(self) -> Self:
        result = type(self)()
        for point, value in self.items():
            result[point.reflect()] = value
        return result

    def rotate(self) -> Self:
        result = type(self)()
        for point, value in self.items():
            result[point.rotate()] = value
        return result

    def mirror(self) -> Self:
        result = type(self)()
        for point, value in self.items():
            result[point.mirror()] = value
        return result

    def xs(self) -> set[int]:
        return set([point.x for point in self.grid])

    def ys(self) -> set[int]:
        return set([point.y for point in self.grid])

    def __setitem__(self, point: Point, value: T) -> None:
        self.grid[point] = value

    def __getitem__(self, point: Point) -> Optional[T]:
        return self.grid.get(point, None)

    def __contains__(self, point: Point) -> bool:
        return point in self.grid

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        rows: list[str] = []
        xs, ys = self.xs(), self.ys()
        for y in range(max(ys), min(ys) - 1, -1):
            row: list[str] = []
            for x in range(min(xs), max(xs) + 1):
                point = Point(x, y)
                value = str(self[point]) if point in self else "."
                row.append(value)
            rows.append("".join(row))
        return "\n".join(rows)
