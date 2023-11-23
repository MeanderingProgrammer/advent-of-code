from dataclasses import dataclass

from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser


@dataclass(frozen=True)
class Art:
    value: list[str]

    def split(self) -> list[list[str]]:
        components: list[list[str]] = []
        size: int = 2 if len(self.value) % 2 == 0 else 3
        for r in range(0, len(self.value), size):
            component_row: list[str] = []
            for c in range(0, len(self.value[r]), size):
                component_row.append(
                    "\n".join([self.value[r + i][c : c + size] for i in range(size)])
                )
            components.append(component_row)
        return components

    def on(self) -> int:
        return sum([sum([v == "#" for v in row]) for row in self.value])


class Pattern:
    def __init__(self, value: str):
        parts = value.split(" => ")
        self.permutations: set[str] = Pattern.permute(parts[0])
        self.output: list[str] = parts[1].split("/")

    def matches(self, component: str) -> bool:
        return component in self.permutations

    @staticmethod
    def permute(value: str) -> set[str]:
        grid = Grid()
        for y, row in enumerate(value.split("/")):
            for x, value in enumerate(row):
                grid[Point(x, y)] = value
        permutations: set[str] = set()
        for _ in range(4):
            permutations.add(str(grid))
            permutations.add(str(grid.reflect()))
            grid = grid.rotate()
        return permutations


def main() -> None:
    patterns = [Pattern(line) for line in Parser().lines()]
    answer.part1(188, run_iterations(patterns, 5))
    answer.part2(2758764, run_iterations(patterns, 18))


def run_iterations(patterns: list[Pattern], n: int):
    art = Art([".#.", "..#", "###"])
    for _ in range(n):
        rows: list[str] = []
        for component_row in art.split():
            new_row: list[list[str]] = []
            for component in component_row:
                pattern = get_matching_pattern(component, patterns)
                new_row.append(pattern.output)
            rows.extend(join_row(new_row))
        art = Art(rows)
    return art.on()


def get_matching_pattern(component: str, patterns: list[Pattern]) -> Pattern:
    for pattern in patterns:
        if pattern.matches(component):
            return pattern
    raise Exception("Failed")


def join_row(row: list[list[str]]) -> list[str]:
    result: list[str] = []
    for i in range(len(row[0])):
        rs: list[str] = []
        for r in row:
            rs.append(r[i])
        result.append("".join(rs))
    return result


if __name__ == "__main__":
    main()
