from aoc_parser import Parser
from aoc_board import Grid, Point
from aoc_graph import Graph
import re


STEP_PATTERN = '^Step (.) must be finished before step (.) can begin.$'


def main():
    file_name = 'data'
    graph = get_graph(file_name)
    solve_part_1(graph)
    solve_part_2(graph)


def solve_part_1(graph):
    # Part 1 = LAPFCRGHVZOTKWENBXIMSUDJQY
    order = graph.topo_sort()
    print('Order String = {}'.format(''.join(order)))


def solve_part_2(graph):
    # Part 2 = 936
    duration = graph.get_duration(5, 60)
    print('Total duration = {}'.format(duration))
    

def get_graph(file_name):
    graph = Graph()
    for line in Parser(file_name).lines():
        match = re.match(STEP_PATTERN, line)
        graph.add_edge(match[2], match[1])
    return graph


if __name__ == '__main__':
    main()

