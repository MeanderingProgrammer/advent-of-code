from collections import deque
from dataclasses import dataclass, field

from aoc import answer
from aoc.parser import Parser
from aoc.point import Point, PointHelper


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
        blocks: list[str] = []
        for value in Knot.dense_hash(list(self.q)):
            blocks.append(bin(int(value, 16))[2:].rjust(4, "0"))
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
        hashed: list[str] = []
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
    points = enabled_points(Parser().string())
    answer.part1(8190, len(points))
    answer.part2(1134, group_points(points))


def enabled_points(prefix: str) -> list[Point]:
    points: list[Point] = []
    for y in range(128):
        knot = Knot(
            q=deque(range(256)),
            lengths=list(map(ord, prefix + "-" + str(y))) + [17, 31, 73, 47, 23],
        )
        hashed = knot.run_hash()
        points.extend([(x, y) for x, value in enumerate(hashed) if value == "1"])
    return points


def group_points(points: list[Point]) -> int:
    groups: list[frozenset[Point]] = []
    for point in points:
        adjacent = set(PointHelper.neighbors(point))
        matching_groups = [group for group in groups if not adjacent.isdisjoint(group)]
        new_group = set([point])
        for group in matching_groups:
            new_group |= group
            groups.remove(group)
        groups.append(frozenset(new_group))
    return len(groups)


if __name__ == "__main__":
    main()
