import hashlib

from aoc import answer
from aoc.parser import Parser
from aoc.point import Point

DIRECTIONS: list[tuple[str, Point]] = [
    ("U", (0, 1)),
    ("D", (0, -1)),
    ("L", (-1, 0)),
    ("R", (1, 0)),
]

LEGAL_HASH: list[str] = ["b", "c", "d", "e", "f"]


@answer.timer
def main() -> None:
    code: str = Parser().string()
    paths: list[str] = bfs(code, (-3, 3), (0, 0))
    answer.part1("DDRLRRUDDR", paths[0])
    answer.part2(556, len(paths[-1]))


def bfs(code: str, start: Point, end: Point) -> list[str]:
    queue: list[tuple[Point, str]] = [(start, "")]
    paths: list[str] = []
    while len(queue) > 0:
        point, path = queue.pop(0)
        if point == end:
            paths.append(path)
        else:
            for adjacent in get_adjacent(code, point, path):
                queue.append(adjacent)
    return paths


def get_adjacent(code: str, point: Point, path: str) -> list[tuple[Point, str]]:
    hashed: str = hashlib.md5(str.encode(code + path)).hexdigest()
    result: list[tuple[Point, str]] = []
    for i, (symbol, direction) in enumerate(DIRECTIONS):
        x, y = (point[0] + direction[0], point[1] + direction[1])
        in_bounds: bool = x >= -3 and x <= 0 and y <= 3 and y >= 0
        if in_bounds and hashed[i] in LEGAL_HASH:
            result.append(((x, y), path + symbol))
    return result


if __name__ == "__main__":
    main()
