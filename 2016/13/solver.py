from dataclasses import dataclass

from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point, PointHelper
from aoc.search import Search


@dataclass(frozen=True)
class Maze:
    grid: Grid[bool]
    favorite_number: int

    def get_adjacent(self, point: Point) -> list[Point]:
        result: set[Point] = set()
        for adjacent in PointHelper.neighbors(point):
            if adjacent[0] >= 0 and adjacent[1] >= 0:
                if adjacent not in self.grid:
                    self.grid[adjacent] = self.is_wall(*adjacent)
                if not self.grid[adjacent]:
                    result.add(adjacent)
        return list(result)

    def is_wall(self, x: int, y: int) -> bool:
        value = (x * x) + (3 * x) + (2 * x * y) + y + y * y
        value += self.favorite_number
        value = bin(value)[2:]
        num_ones = sum([v == "1" for v in value])
        return num_ones % 2 == 1


@answer.timer
def main() -> None:
    maze = Maze(grid=dict(), favorite_number=Parser().integer())
    start: Point = (1, 1)
    search = Search[Point](
        start=start,
        end=(31, 39),
        neighbors=maze.get_adjacent,
    )
    answer.part1(92, search.bfs())
    answer.part2(124, len(reachable(start, 50, maze)))


def reachable(start: Point, maximum: int, maze: Maze) -> set[Point]:
    queue: list[tuple[int, Point]] = [(0, start)]
    seen: set[Point] = set()
    while len(queue) > 0:
        length, position = queue.pop(0)
        if position in seen:
            continue
        seen.add(position)
        for adjacent in maze.get_adjacent(position):
            if adjacent not in seen and length < maximum:
                queue.append((length + 1, adjacent))
    return seen


if __name__ == "__main__":
    main()
