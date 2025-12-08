import heapq
from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class NanoBot:
    x: int
    y: int
    z: int
    r: int

    @classmethod
    def new(cls, s: str) -> Self:
        # pos=<1,-2,3>, r=4
        pos, r = s.split(", ")
        x, y, z = pos.split("=")[1][1:-1].split(",")
        _, r = r.split("=")
        return cls(
            x=int(x),
            y=int(y),
            z=int(z),
            r=int(r),
        )

    def __contains__(self, o: Self) -> bool:
        dx, dy, dz = self.x - o.x, self.y - o.y, self.z - o.z
        return abs(dx) + abs(dy) + abs(dz) <= self.r

    def __len__(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)


@answer.timer
def main() -> None:
    bots = [NanoBot.new(line) for line in Parser().lines()]
    bots.sort(key=lambda bot: bot.r)
    strongest = bots[-1]
    answer.part1(383, sum([bot in strongest for bot in bots]))
    answer.part2(100474026, distance_of_most_overlap(bots))


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

    distances: dict[int, set[int]] = defaultdict(set)
    bots_in_range = 0
    while len(queue) > 0:
        distance, add = heapq.heappop(queue)
        bots_in_range += 1 if add else -1
        distances[bots_in_range].add(distance)

    return min(distances[max(distances)])


if __name__ == "__main__":
    main()
