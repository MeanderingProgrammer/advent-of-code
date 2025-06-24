from dataclasses import dataclass

from aoc import answer
from aoc.grid import Grid, GridHelper
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


@answer.timer
def main() -> None:
    patterns = get_patterns()
    answer.part1(188, run_iterations(patterns, 5))
    answer.part2(2758764, run_iterations(patterns, 18))


def get_patterns() -> dict[str, list[str]]:
    patterns: dict[str, list[str]] = dict()
    for line in Parser().lines():
        parts: list[str] = line.split(" => ")
        output: list[str] = parts[1].split("/")
        grid: Grid[str] = dict()
        for y, row in enumerate(parts[0].split("/")):
            for x, value in enumerate(row):
                grid[(x, y)] = value
        for _ in range(4):
            patterns[GridHelper.to_str(grid)] = output
            patterns[GridHelper.to_str(GridHelper.reflect(grid))] = output
            grid = GridHelper.rotate(grid)
    return patterns


def run_iterations(patterns: dict[str, list[str]], n: int) -> int:
    art = Art([".#.", "..#", "###"])
    for _ in range(n):
        rows: list[str] = []
        for component_row in art.split():
            new_row: list[list[str]] = [
                patterns[component] for component in component_row
            ]
            rows.extend(join_row(new_row))
        art = Art(rows)
    return art.on()


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
