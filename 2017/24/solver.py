from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class Bridge:

    def __init__(self, components):
        self.components = components

    def build(self):
        statistics = []
        for bridge in self.generate():
            statistics.append(
                (len(bridge), self.strength(bridge))
            )
        return statistics

    def generate(self, bridge=None):
        bridge = bridge or []
        current_end = bridge[-1][1] if len(bridge) > 0 else 0
        for new_end in self.components[current_end]:
            if not self.contains(current_end,new_end, bridge):
                new_bridge = bridge + [(current_end, new_end)]
                yield new_bridge
                yield from self.generate(new_bridge)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {}'.format(self.components, self.needed)

    @staticmethod
    def contains(start, end, bridge):
        return (start, end) in bridge or (end, start) in bridge

    @staticmethod
    def strength(bridge):
        return sum([component[0] + component[1] for component in bridge])


def main():
    components = get_components()
    bridge = Bridge(components)
    statistics = bridge.build()
    # Part 1 = 1656
    print(get_strongest(statistics))
    # Part 2 = 1642
    print(get_longest_strongest(statistics))


def get_strongest(statistics):
    return max([stat[1] for stat in statistics])


def get_longest_strongest(statistics):
    longest = max([stat[0] for stat in statistics])
    all_longest = [stat for stat in statistics if stat[0] == longest]
    return get_strongest(all_longest)


def get_components():
    components = defaultdict(set)
    for line in Parser(FILE_NAME).lines():
        p1, p2 = [int(x) for x in line.split('/')]
        components[p1].add(p2)
        components[p2].add(p1)
    return components


if __name__ == '__main__':
    main()

