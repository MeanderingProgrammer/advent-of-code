from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


def main():
    graph = get_graph()
    
    # Part 1 = 306
    connected_to_0 = aoc_search.connected(graph, '0')
    print('Total reachable = {}'.format(len(connected_to_0)))

    # Part 2 = 200
    heads = set(['0'])
    grouped = set(connected_to_0)

    head = get_ungrouped(graph, grouped)
    while head is not None:
        heads.add(head)
        connected = aoc_search.connected(graph, head)
        grouped |= connected
        head = get_ungrouped(graph, grouped)

    print('Total groups = {}'.format(len(heads)))


def get_ungrouped(graph, grouped):
    all_keys = set(graph.keys())
    remainder = all_keys - grouped
    return None if len(remainder) == 0 else next(iter(remainder))


def get_graph():
    graph = defaultdict(set)
    for line in Parser(FILE_NAME).lines():
        parts = line.split(' <-> ')
        start = parts[0]
        for end in parts[1].split(', '):
            graph[start].add(end)
    return graph


if __name__ == '__main__':
    main()
