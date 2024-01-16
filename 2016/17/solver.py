import hashlib

from aoc import answer, search
from aoc.parser import Parser
from aoc.point import Direction, Point, PointHelper

DIRECTIONS: list[str] = ["U", "D", "L", "R"]


@answer.timer
def main() -> None:
    code = Parser(strip=True).string()
    paths = search.bfs_paths(((-3, 3), code), (0, 0), get_adjacent)
    answer.part1("DDRLRRUDDR", pull_path(code, paths[0]))
    answer.part2(556, len(pull_path(code, paths[-1])))


def get_adjacent(item: tuple[Point, str]) -> list[tuple[Point, str]]:
    point, code = item
    hashed = hash(code)
    result: list[tuple[Point, str]] = []
    for i, name in enumerate(DIRECTIONS):
        next_point = PointHelper.go(point, Direction.from_str(name))
        if is_legal(next_point) and unlocked(hashed[i]):
            result.append((next_point, code + name))
    return result


def is_legal(p: Point) -> bool:
    return p[0] >= -3 and p[0] <= 0 and p[1] <= 3 and p[1] >= 0


def unlocked(value: str) -> bool:
    return value in ["b", "c", "d", "e", "f"]


def hash(value: str) -> str:
    return hashlib.md5(str.encode(value)).hexdigest()[:4]


def pull_path(code: str, value: str) -> str:
    return value[len(code) :]


if __name__ == "__main__":
    main()
