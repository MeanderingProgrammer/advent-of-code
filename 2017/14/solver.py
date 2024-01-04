from collections import deque
from dataclasses import dataclass, field

from aoc import answer
from aoc.parser import Parser

Point = tuple[int, int]
DIRECTIONS: list[Point] = [(0, 1), (0, -1), (1, 0), (-1, 0)]


@dataclass
class Knot:
    q: deque[int]
    lengths: list[int]
    skip_size: int = 0
    skipped: list[int] = field(default_factory=list)

    def run_hash(self) -> str:
        for _ in range(64):
            self.run()
        self.q.rotate(sum(self.skipped))
        blocks = [
            bin(int(value, 16))[2:].rjust(4, "0")
            for value in Knot.dense_hash(list(self.q))
        ]
        return "".join(blocks)

    def run(self) -> None:
        for length in self.lengths:
            temp = [self.q.popleft() for _ in range(length)]
            temp.reverse()
            self.q.extend(temp)
            self.q.rotate(-self.skip_size)
            self.skipped.append(length + self.skip_size)
            self.skip_size += 1

    @staticmethod
    def dense_hash(values: list[int]) -> str:
        hashed = []
        for i in range(0, len(values), 16):
            block = values[i : i + 16]
            hashed.append(Knot.hash_block(block))
        return "".join(hashed)

    @staticmethod
    def hash_block(values: list[int]) -> str:
        hashed = 0
        for value in values:
            hashed ^= value
        return hex(hashed)[2:].rjust(2, "0")


@answer.timer
def main() -> None:
    points = enabled_points(Parser(strip=True).string())
    answer.part1(8190, len(points))
    answer.part2(1134, len(group_points(points)))


def enabled_points(prefix: str) -> list[Point]:
    points: list[Point] = []
    for y in range(128):
        hashed = Knot(
            q=deque(range(256)),
            lengths=list(map(ord, prefix + "-" + str(y))) + [17, 31, 73, 47, 23],
        ).run_hash()
        points.extend([(x, y) for x, value in enumerate(hashed) if value == "1"])
    return points


def group_points(points: list[Point]) -> set[frozenset[Point]]:
    groups: set[frozenset[Point]] = set()
    for point in points:
        adjacent = set([(point[0] + dx, point[1] + dy) for dy, dx in DIRECTIONS])
        matching_groups = [group for group in groups if adjacent & group]
        new_group = set([point])
        for group in matching_groups:
            new_group |= group
            groups.remove(group)
        groups.add(frozenset(new_group))
    return groups


if __name__ == "__main__":
    main()
