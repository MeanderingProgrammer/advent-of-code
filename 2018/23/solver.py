import heapq
from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser

type Point3d = tuple[int, int, int]


@dataclass(frozen=True)
class NanoBot:
    pos: Point3d
    r: int

    def in_range(self, o: Self) -> bool:
        x1, y1, z1 = self.pos
        x2, y2, z2 = o.pos
        return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) <= self.r

    def __len__(self) -> int:
        x, y, z = self.pos
        return abs(x) + abs(y) + abs(z)


@answer.timer
def main() -> None:
    bots = get_bots()
    bots.sort(key=lambda bot: bot.r)
    strongest_bot = bots[-1]
    answer.part1(383, sum([strongest_bot.in_range(bot) for bot in bots]))
    answer.part2(100474026, distance_of_most_overlap(bots))


def get_bots() -> list[NanoBot]:
    def parse_bot(line: str) -> NanoBot:
        pos, radius = line.split(", ")
        coords = [int(c) for c in pos.split("=")[1][1:-1].split(",")]
        assert len(coords) == 3
        return NanoBot(
            pos=(coords[0], coords[1], coords[2]),
            r=int(radius.split("=")[1]),
        )

    return [parse_bot(line) for line in Parser().lines()]


def distance_of_most_overlap(bots: list[NanoBot]) -> int:
    # A copy of: https://github.com/tterb/advent-of-code/blob/master/2018/day23.py
    queue: list[tuple[int, bool]] = []

    # One key piece of information is that the minimum distance from the origin is guaranteed
    # to be on the edge of one of the bots, i.e. its manhattan distance minus its radius
    for bot in bots:
        # Positions that have a manhattan distance larger than bots manhattan
        # distance minus radius will be included by this bots radius
        heapq.heappush(queue, (len(bot) - bot.r, True))
        # Positions that have a manhattan distance larger than the bots manhattan
        # distance plus its radius are no longer in the range of this bot
        heapq.heappush(queue, (len(bot) + bot.r + 1, False))

    bots_in_range = 0
    in_range_distances: dict[int, set[int]] = defaultdict(set)
    while len(queue) > 0:
        distance, add = heapq.heappop(queue)
        bots_in_range += 1 if add else -1
        in_range_distances[bots_in_range].add(distance)

    max_in_range = max(in_range_distances.keys())
    distances = in_range_distances[max_in_range]
    return min(distances)


if __name__ == "__main__":
    main()
