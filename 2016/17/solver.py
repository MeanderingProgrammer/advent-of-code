import hashlib
from typing import List, Tuple

from aoc import answer, search
from aoc.board import Point

CODE = "udskfozm"


DIRECTIONS = [
    (Point(0, 1), "U"),
    (Point(0, -1), "D"),
    (Point(-1, 0), "L"),
    (Point(1, 0), "R"),
]


def main() -> None:
    paths = search.bfs_paths((Point(-3, 3), CODE), Point(0, 0), get_adjacent)
    answer.part1("DDRLRRUDDR", pull_path(paths[0]))
    answer.part2(556, len(pull_path(paths[-1])))


def get_adjacent(item: Tuple[Point, str]) -> List[Tuple[Point, str]]:
    point, code = item
    hashed = hash(code)
    result = []
    for i, direction in enumerate(DIRECTIONS):
        new_point = point + direction[0]
        if is_legal(new_point) and unlocked(hashed[i]):
            result.append((new_point, code + direction[1]))
    return result


def is_legal(p: Point) -> bool:
    return p.x() >= -3 and p.x() <= 0 and p.y() <= 3 and p.y() >= 0


def unlocked(value):
    return value in ["b", "c", "d", "e", "f"]


def hash(value):
    return hashlib.md5(str.encode(value)).hexdigest()[:4]


def pull_path(value):
    return value[len(CODE) :]


if __name__ == "__main__":
    main()
