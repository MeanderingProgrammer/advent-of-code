import hashlib

from aoc import answer, search
from aoc.parser import Parser

Point = tuple[int, int]

DIRECTIONS: list[tuple[Point, str]] = [
    ((0, 1), "U"),
    ((0, -1), "D"),
    ((-1, 0), "L"),
    ((1, 0), "R"),
]


def main() -> None:
    code = Parser(strip=True).string()
    paths = search.bfs_paths(((-3, 3), code), (0, 0), get_adjacent)
    answer.part1("DDRLRRUDDR", pull_path(code, paths[0]))
    answer.part2(556, len(pull_path(code, paths[-1])))


def get_adjacent(item: tuple[Point, str]) -> list[tuple[Point, str]]:
    point, code = item
    hashed = hash(code)
    result = []
    for i, (direction, name) in enumerate(DIRECTIONS):
        x, y = point[0] + direction[0], point[1] + direction[1]
        if is_legal(x, y) and unlocked(hashed[i]):
            result.append(((x, y), code + name))
    return result


def is_legal(x: int, y: int) -> bool:
    return x >= -3 and x <= 0 and y <= 3 and y >= 0


def unlocked(value: str) -> bool:
    return value in ["b", "c", "d", "e", "f"]


def hash(value: str) -> str:
    return hashlib.md5(str.encode(value)).hexdigest()[:4]


def pull_path(code: str, value: str) -> str:
    return value[len(code) :]


if __name__ == "__main__":
    main()
