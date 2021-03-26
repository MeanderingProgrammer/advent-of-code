import re

from aoc_parser import Parser
from aoc_graph import Graph


STEP_PATTERN = '^Step (.) must be finished before step (.) can begin.$'


def main():
    file_name = 'data'
    graph = get_graph(file_name)
    # Part 1: LAPFCRGHVZOTKWENBXIMSUDJQY
    print('Part 1: {}'.format(solve_part_1(graph)))
    # Part 2: 936
    print('Part 2: {}'.format(solve_part_2(graph)))


def solve_part_1(graph):
    order = graph.topo_sort()
    return ''.join(order)


def solve_part_2(graph):
    return graph.get_duration(5, 60)
    

def get_graph(file_name):
    graph = Graph()
    for line in Parser(file_name).lines():
        match = re.match(STEP_PATTERN, line)
        graph.add_edge(match[2], match[1])
    return graph


if __name__ == '__main__':
    main()
