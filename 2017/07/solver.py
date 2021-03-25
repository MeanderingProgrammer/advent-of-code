from aoc_parser import Parser
from aoc_board import Grid, Point, Graph


FILE_NAME = 'data'


class Node:

    def __init__(self, value):
        value = value.split()
        self.id = value[0]
        self.weight = int(value[1][1:-1])

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {}'.format(self.id, self.weight)


def main():
    graph = get_graph()
    # Part 1: xegshds
    top_most = graph.top_most()
    print('Part 1: {}'.format(top_most))
    # Part 2: 299
    graph.get_weight(graph.get_node(top_most))
    print('Part 2: {}'.format(graph.to_change))


def get_graph():
    graph = Graph()
    for line in Parser(FILE_NAME).lines():
        line = line.split(' -> ')

        node = Node(line[0])
        graph.add_node(node)

        if len(line) == 2:
            for edge in line[1].split(', '):
                graph.add_edge(node, edge)
    return graph


if __name__ == '__main__':
    main()
