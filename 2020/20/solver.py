from dataclasses import dataclass
from typing import Optional, Self

from aoc import answer
from aoc.parser import Parser


class ImageTile:
    def __init__(self, data: list[str], identifier: Optional[int] = None):
        if identifier is None:
            self.identifier: int = int(data[0][5:-1])
            self.data: list[str] = data[1:]
        else:
            self.identifier: int = identifier
            self.data: list[str] = data
        self.edges: list[str] = [
            "".join(row[0] for row in self.data),  # LEFT
            self.data[0],  # TOP
            "".join(row[-1] for row in self.data),  # RIGHT
            self.data[-1],  # BOTTOM
        ]

    def remove_boarder(self) -> Self:
        boarderless = [row[1:-1] for row in self.data[1:-1]]
        return type(self)(boarderless, self.identifier)

    def add_horizontal(self, other: Self) -> Self:
        combined = [self.data[i] + other.data[i] for i in range(len(self.data))]
        return type(self)(combined, self.identifier)

    def add_vertical(self, other: Self) -> Self:
        combined = self.data + other.data
        return type(self)(combined, self.identifier)

    def all_permutations(self) -> None:
        self.permutations: list[Self] = []
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
        return type(self)(rotated, self.identifier)

    def flip(self) -> Self:
        size = len(self.data)
        rotated = [[str(j) for j in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                rotated[i][size - 1 - j] = self.data[i][j]
        rotated = ["".join(row) for row in rotated]
        return type(self)(rotated, self.identifier)

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
class PuzzleBoard:
    board: dict[tuple[int, int], ImageTile]

    def add(self, tile: ImageTile) -> bool:
        if len(self.board) == 0:
            self.board[(0, 0)] = tile
            return True

        for available in self.get_all_available():
            edges_needed = self.get_edges_needed(available)
            for permutation in tile.permutations:
                if PuzzleBoard.matches(permutation, edges_needed):
                    self.board[available] = permutation
                    return True
        return False

    def get_all_available(self) -> set[tuple[int, int]]:
        available: set[tuple[int, int]] = set()
        for position in self.board:
            available.update(PuzzleBoard.get_adjacent(position))
        return available

    def get_edges_needed(self, position: tuple[int, int]) -> list[Optional[str]]:
        edges_needed: list[Optional[str]] = []
        for i, adjacent in enumerate(self.get_adjacent(position)):
            opposing_edge = (i + 2) % 4
            if adjacent in self.board:
                edges_needed.append(self.board[adjacent].edges[opposing_edge])
            else:
                edges_needed.append(None)
        return edges_needed

    def coalesce(self) -> ImageTile:
        xs = []
        ys = []
        for position in self.board:
            xs.append(position[0])
            ys.append(position[1])
        rows = []
        for y in range(max(ys), min(ys) - 1, -1):
            row = self.board[(min(xs), y)].remove_boarder()
            for x in range(min(xs) + 1, max(xs) + 1):
                row = row.add_horizontal(self.board[(x, y)].remove_boarder())
            rows.append(row)
        combined: ImageTile = rows[0]
        for i in range(1, len(rows)):
            combined = combined.add_vertical(rows[i])
        return combined

    @staticmethod
    def get_adjacent(position: tuple[int, int]) -> list[tuple[int, int]]:
        return [
            (position[0] - 1, position[1]),  # LEFT
            (position[0], position[1] + 1),  # TOP
            (position[0] + 1, position[1]),  # RIGHT
            (position[0], position[1] - 1),  # BOTTOM
        ]

    @staticmethod
    def matches(tile: ImageTile, edges_needed: list[Optional[str]]) -> bool:
        for i, edge in enumerate(tile.edges):
            needed = edges_needed[i]
            if needed is not None:
                if needed != edge:
                    return False
        return True


class SearchImage:
    def __init__(self, image: list[str]):
        self.dimensions: tuple[int, int] = (len(image[0]), len(image))
        self.points: list[tuple[int, int]] = SearchImage.get_positive_points(image)

    def find_num_matches(self, tile: ImageTile) -> int:
        num_matches = 0
        for starting_point in self.starting_points(tile.dimensions()):
            cropped = self.crop(starting_point, tile)
            if self.does_match(cropped):
                num_matches += 1
        return num_matches

    def starting_points(self, dimensions: tuple[int, int]) -> list[tuple[int, int]]:
        max_x = dimensions[0] - self.dimensions[0]
        max_y = dimensions[1] - self.dimensions[1]

        starting_points: list[tuple[int, int]] = []
        for x in range(max_x):
            for y in range(max_y):
                starting_points.append((x, y))
        return starting_points

    def crop(self, point: tuple[int, int], tile: ImageTile) -> list[str]:
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
    def get_positive_points(image: list[str]) -> list[tuple[int, int]]:
        positive_points: list[tuple[int, int]] = []
        for row in range(len(image)):
            for col in range(len(image[row])):
                value = image[row][col]
                if value == "#":
                    positive_points.append((col, row))
        return positive_points


def main() -> None:
    board = PuzzleBoard(board=dict())
    solve_board(board)
    answer.part1(15003787688423, corner_values(board))
    answer.part2(1705, get_roughness(board))


def solve_board(board: PuzzleBoard) -> None:
    image_tiles = [ImageTile(group) for group in Parser().line_groups()]
    [image_tile.all_permutations() for image_tile in image_tiles]
    remaining_tiles = image_tiles
    while len(remaining_tiles) != 0:
        still_remaining = []
        for tile in remaining_tiles:
            if not board.add(tile):
                still_remaining.append(tile)
        remaining_tiles = still_remaining


def corner_values(board: PuzzleBoard) -> int:
    xs = []
    ys = []
    for position in board.board:
        xs.append(position[0])
        ys.append(position[1])
    corners = [
        board.board[(min(xs), min(ys))].identifier,
        board.board[(min(xs), max(ys))].identifier,
        board.board[(max(xs), min(ys))].identifier,
        board.board[(max(xs), max(ys))].identifier,
    ]
    value = 1
    for corner in corners:
        value *= corner
    return value


def get_roughness(board: PuzzleBoard) -> int:
    search_image = SearchImage(Parser(file_name="sea-monster").lines())
    search_positive = len(search_image.points)

    image = board.coalesce()
    image_positive = image.get_num_positive()
    image.all_permutations()

    for permutation in image.permutations:
        num_matches = search_image.find_num_matches(permutation)
        if num_matches > 0:
            return image_positive - (num_matches * search_positive)

    raise Exception("Failed")


if __name__ == "__main__":
    main()
