from dataclasses import dataclass

from aoc import answer, search
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point, PointHelper


@dataclass(frozen=True)
class Maze:
    grid: Grid
    favorite_number: int

    def get_adjacent(self, point: Point) -> list[Point]:
        result = set()
        for adjacent in PointHelper.neighbors(point):
            if adjacent[0] >= 0 and adjacent[1] >= 0:
                if adjacent not in self.grid:
                    self.grid[adjacent] = self.is_wall(adjacent)
                if not self.grid[adjacent]:
                    result.add(adjacent)
        return list(result)

    def is_wall(self, point: Point) -> bool:
        x, y = point
        value = (x * x) + (3 * x) + (2 * x * y) + y + y * y
        value += self.favorite_number
        value = bin(value)[2:]
        num_ones = sum([v == "1" for v in value])
        return num_ones % 2 == 1


@answer.timer
def main() -> None:
    maze = Maze(grid=dict(), favorite_number=Parser().integer())
    start, goal = (1, 1), (31, 39)
    answer.part1(92, search.bfs(start, goal, maze.get_adjacent))
    answer.part2(124, len(search.reachable(start, 50, maze.get_adjacent)))


if __name__ == "__main__":
    main()
