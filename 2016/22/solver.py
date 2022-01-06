import commons.answer as answer
import commons.aoc_search as aoc_search
from commons.aoc_board import Grid, Point
from commons.aoc_parser import Parser


class Node:

    def __init__(self, total, used, available):
        self.total = self.parse_size(total)
        self.used = self.parse_size(used)
        self.available = self.parse_size(available)

    def empty(self):
        return self.used == 0

    def can_store(self, o):
        return self.available >= o.used

    def coult_store(self, o):
        return self.total >= o.used

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({0: <3}/{1: <3})'.format(self.used, self.total)

    @staticmethod
    def parse_size(size):
        return int(size[:-1])


def main():
    nodes = get_nodes()
    answer.part1(910, get_viable_connections(nodes))
    answer.part2(222, calculate_transfers(nodes))


def calculate_transfers(nodes):
    xs = nodes.xs()

    goal_node = Point(max(xs) - 1, 1)
    free_node = get_free_node(nodes)
    moves_needed_to_free = aoc_search.bfs(free_node, goal_node, get_adjacent(nodes))

    horizontal_transfers = max(xs) - 1
    # Amount of movements needed to get free space above node to the left of goal
    # 2 movements to move freed space and transfer goal
    # Each horizontal transfer requires 5 movements
    return moves_needed_to_free + 2 + horizontal_transfers * 5


def get_free_node(nodes):
    for position, node in nodes.items():
        if node.empty():
            return position


def get_adjacent(nodes):
    def actual(position):
        result, value = [], nodes[position]
        for adj in position.adjacent():
            if adj in nodes:
                adj_value = nodes[adj]
                if value.coult_store(adj_value):
                    result.append(adj)
        return result
    return actual


def get_viable_connections(nodes):
    viable = []
    for p1, n1 in nodes.items():
        for p2, n2 in nodes.items():
            if are_viable(n1, n2):
                viable.append((n1, n2))
    return len(viable)


def are_viable(n1, n2):
    if n1.empty():
        return False
    if n1 == n2:
        return False
    return n2.can_store(n1)


def get_nodes():
    nodes = Grid()
    for line in Parser().lines()[2:]:
        node, total, used, available, use = line.split()
        nodes[parse_node(node)] = Node(total, used, available)
    return nodes


def parse_node(node):
    node = node.split('/')[3].split('-')
    x = int(node[1][1:])
    y = int(node[2][1:])
    return Point(x, y)


if __name__ == '__main__':
    main()
