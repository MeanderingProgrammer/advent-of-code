from aoc import answer
from aoc.parser import Parser
from collections import defaultdict


class Orbits:
    def __init__(self):
        self.orbits = defaultdict(list)

    def add(self, orbit):
        orbit = orbit.split(")")
        self.orbits[orbit[0]].append(orbit[1])

    def get_distance(self, start, finish):
        explored = set()
        to_explore = [(start, -1)]

        for orbit, value in to_explore:
            for adjacent in self.get_adjacent(orbit):
                if adjacent == finish:
                    return value
                elif adjacent not in explored:
                    to_explore.append((adjacent, value + 1))
            explored.add(orbit)

    def get_adjacent(self, node):
        adjacent = [value for value in self.orbits[node]]
        for k, v in self.orbits.items():
            if node in v:
                adjacent.append(k)
        return adjacent

    def __len__(self):
        count = 0

        to_explore = [("COM", 0)]
        for orbit, value in to_explore:
            count += value
            for adjacent in self.orbits[orbit]:
                to_explore.append((adjacent, value + 1))

        return count

    def __str__(self):
        return str(self.orbits)


def main():
    orbits = get_orbits()
    answer.part1(358244, len(orbits))
    answer.part2(517, orbits.get_distance("YOU", "SAN"))


def get_orbits():
    orbits = Orbits()
    for orbit in Parser().lines():
        orbits.add(orbit)
    return orbits


if __name__ == "__main__":
    main()
