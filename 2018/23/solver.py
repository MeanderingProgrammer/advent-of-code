import heapq
from collections import defaultdict

from aoc import answer
from aoc.board import Point
from aoc.parser import Parser


class NanoBot:
    def __init__(self, value):
        pos, radius = value.split(", ")
        self.pos = Point(*[int(c) for c in pos.split("=")[1][1:-1].split(",")])
        self.r = int(radius.split("=")[1])

    def in_range(self, o):
        diff = self.pos - o
        return len(diff) <= self.r

    def __len__(self):
        return len(self.pos)

    def __lt__(self, o):
        return self.r < o.r

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{}, {}".format(self.pos, self.r)


def main():
    bots = get_bots()
    bots.sort()

    strongest_bot = bots[-1]
    bots_in_range = [bot for bot in bots if strongest_bot.in_range(bot.pos)]

    answer.part1(383, len(bots_in_range))
    answer.part2(100474026, distance_of_most_overlap(bots))


def distance_of_most_overlap(bots):
    # A copy of: https://github.com/tterb/advent-of-code/blob/master/2018/day23.py
    queue = []

    # One key piece of information is that the minimum distance from the origin is
    # guaranteed to be on the edge of one of the bots, i.e. its manhattan distance,
    # minus its radius
    for bot in bots:
        # Positions that have a manhattan distance larger than bots manhattan
        # distance minus radius will be included by this bots radius
        heapq.heappush(queue, (len(bot) - bot.r, True))
        # Positions that have a manhattan distance larger than the bots manhattan
        # distance plus its radius are no longer in the range of this bot
        heapq.heappush(queue, (len(bot) + bot.r + 1, False))

    bots_in_range, in_range_distances = 0, defaultdict(set)
    while len(queue) > 0:
        distance, add = heapq.heappop(queue)
        bots_in_range += 1 if add else -1
        in_range_distances[bots_in_range].add(distance)

    max_in_range = max(in_range_distances.keys())
    distances = in_range_distances[max_in_range]
    return min(distances)


def get_bots():
    return [NanoBot(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
