from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Triangle:
    values: list[str]

    def valid(self) -> bool:
        sides = [int(value) for value in self.values]
        sides.sort()
        return (sides[0] + sides[1]) > sides[2]


@answer.timer
def main() -> None:
    answer.part1(862, num_valid(vertically()))
    answer.part2(1577, num_valid(horizontally()))


def num_valid(triangles: list[Triangle]) -> int:
    return sum([triangle.valid() for triangle in triangles])


def vertically() -> list[Triangle]:
    return [Triangle(line.split()) for line in get_lines()]


def horizontally() -> list[Triangle]:
    triangles: list[Triangle] = []
    lines = get_lines()
    for i in range(0, len(lines), 3):
        top_3 = [line.split() for line in lines[i : i + 3]]
        for j in range(3):
            sides = [line[j] for line in top_3]
            triangles.append(Triangle(sides))
    return triangles


def get_lines() -> list[str]:
    return Parser().lines()


if __name__ == "__main__":
    main()
