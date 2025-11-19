from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.grid import Grid
from aoc.parser import Parser
from aoc.point import Point


class Tile:
    def __init__(self, id: int, data: list[str]):
        self.id: int = id
        self.data: list[str] = data
        self.edges: list[str] = [
            "".join(row[0] for row in self.data),  # LEFT
            self.data[0],  # TOP
            "".join(row[-1] for row in self.data),  # RIGHT
            self.data[-1],  # BOTTOM
        ]
        self.permutations: list[Self] = []

    def remove_boarder(self) -> Self:
        boarderless = [row[1:-1] for row in self.data[1:-1]]
        return type(self)(self.id, boarderless)

    def add_horizontal(self, other: Self) -> Self:
        combined = [self.data[i] + other.data[i] for i in range(len(self.data))]
        return type(self)(self.id, combined)

    def add_vertical(self, other: Self) -> Self:
        combined = self.data + other.data
        return type(self)(self.id, combined)

    def all_permutations(self) -> None:
        tile = self
        for _ in range(4):
            tile = tile.rotate()
            self.permutations.append(tile)
        tile = self.flip()
        for _ in range(4):
            tile = tile.rotate()
            self.permutations.append(tile)

    def rotate(self) -> Self:
        size = len(self.data)
        rotated = [[str(j) for j in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                rotated[size - 1 - j][i] = self.data[i][j]
        rotated = ["".join(row) for row in rotated]
        return type(self)(self.id, rotated)

    def flip(self) -> Self:
        size = len(self.data)
        rotated = [[str(j) for j in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                rotated[i][size - 1 - j] = self.data[i][j]
        rotated = ["".join(row) for row in rotated]
        return type(self)(self.id, rotated)

    def get_num_positive(self) -> int:
        num_positive = 0
        for row in self.data:
            for value in row:
                if value == "#":
                    num_positive += 1
        return num_positive

    def dimensions(self) -> tuple[int, int]:
        return len(self.data[0]), len(self.data)


@dataclass(frozen=True)
class Puzzle:
    board: Grid[Tile]

    def add(self, tile: Tile) -> bool:
        if len(self.board) == 0:
            self.board[(0, 0)] = tile
            return True

        for available in self.get_all_available():
            edges_needed = self.get_edges_needed(available)
            for permutation in tile.permutations:
                if Puzzle.matches(permutation, edges_needed):
                    self.board[available] = permutation
                    return True
        return False

    def get_all_available(self) -> set[Point]:
        available: set[Point] = set()
        for position in self.board:
            available.update(Puzzle.get_adjacent(position))
        return available

    def get_edges_needed(self, position: Point) -> list[str | None]:
        edges_needed: list[str | None] = []
        for i, adjacent in enumerate(Puzzle.get_adjacent(position)):
            opposing_edge = (i + 2) % 4
            if adjacent in self.board:
                edges_needed.append(self.board[adjacent].edges[opposing_edge])
            else:
                edges_needed.append(None)
        return edges_needed

    def coalesce(self) -> Tile:
        xs: list[int] = []
        ys: list[int] = []
        for position in self.board:
            xs.append(position[0])
            ys.append(position[1])
        rows: list[Tile] = []
        for y in range(max(ys), min(ys) - 1, -1):
            row = self.board[(min(xs), y)].remove_boarder()
            for x in range(min(xs) + 1, max(xs) + 1):
                row = row.add_horizontal(self.board[(x, y)].remove_boarder())
            rows.append(row)
        combined: Tile = rows[0]
        for i in range(1, len(rows)):
            combined = combined.add_vertical(rows[i])
        return combined

    @staticmethod
    def get_adjacent(position: Point) -> list[Point]:
        return [
            (position[0] - 1, position[1]),  # LEFT
            (position[0], position[1] + 1),  # TOP
            (position[0] + 1, position[1]),  # RIGHT
            (position[0], position[1] - 1),  # BOTTOM
        ]

    @staticmethod
    def matches(tile: Tile, edges_needed: list[str | None]) -> bool:
        for i, edge in enumerate(tile.edges):
            needed = edges_needed[i]
            if needed is not None:
                if needed != edge:
                    return False
        return True


class Search:
    def __init__(self, image: list[str]):
        self.dimensions: tuple[int, int] = (len(image[0]), len(image))
        self.points: list[Point] = Search.get_positive_points(image)

    def find_num_matches(self, tile: Tile) -> int:
        num_matches = 0
        for starting_point in self.starting_points(tile.dimensions()):
            cropped = self.crop(starting_point, tile)
            if self.does_match(cropped):
                num_matches += 1
        return num_matches

    def starting_points(self, dimensions: tuple[int, int]) -> list[Point]:
        max_x = dimensions[0] - self.dimensions[0]
        max_y = dimensions[1] - self.dimensions[1]

        starting_points: list[Point] = []
        for x in range(max_x):
            for y in range(max_y):
                starting_points.append((x, y))
        return starting_points

    def crop(self, point: Point, tile: Tile) -> list[str]:
        cropped: list[str] = []
        for i in range(self.dimensions[1]):
            row = tile.data[i + point[1]]
            cropped.append(row[point[0] : point[0] + self.dimensions[0]])
        return cropped

    def does_match(self, image: list[str]) -> bool:
        for point in self.points:
            value = image[point[1]][point[0]]
            if value != "#":
                return False
        return True

    @staticmethod
    def get_positive_points(image: list[str]) -> list[Point]:
        positive_points: list[Point] = []
        for row in range(len(image)):
            for col in range(len(image[row])):
                value = image[row][col]
                if value == "#":
                    positive_points.append((col, row))
        return positive_points


@answer.timer
def main() -> None:
    groups = Parser().line_groups()
    puzzle = Puzzle(board=dict())
    tiles = [Tile(int(group[0][5:-1]), group[1:]) for group in groups]
    [tile.all_permutations() for tile in tiles]
    remaining = tiles
    while len(remaining) != 0:
        still_remaining: list[Tile] = []
        for tile in remaining:
            if not puzzle.add(tile):
                still_remaining.append(tile)
        remaining = still_remaining

    answer.part1(15003787688423, corner_values(puzzle))
    answer.part2(1705, get_roughness(puzzle))


def corner_values(puzzle: Puzzle) -> int:
    xs: list[int] = []
    ys: list[int] = []
    for position in puzzle.board:
        xs.append(position[0])
        ys.append(position[1])
    corners = [
        puzzle.board[(min(xs), min(ys))].id,
        puzzle.board[(min(xs), max(ys))].id,
        puzzle.board[(max(xs), min(ys))].id,
        puzzle.board[(max(xs), max(ys))].id,
    ]
    value = 1
    for corner in corners:
        value *= corner
    return value


def get_roughness(puzzle: Puzzle) -> int:
    search_image = Search(Parser(file_name="sea-monster.txt").lines())
    search_positive = len(search_image.points)

    image = puzzle.coalesce()
    image_positive = image.get_num_positive()
    image.all_permutations()

    for permutation in image.permutations:
        num_matches = search_image.find_num_matches(permutation)
        if num_matches > 0:
            return image_positive - (num_matches * search_positive)

    raise Exception("Failed")


if __name__ == "__main__":
    main()
