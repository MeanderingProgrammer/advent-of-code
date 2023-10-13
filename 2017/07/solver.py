from aoc import answer
from aoc.parser import Parser


class Graph:
    def __init__(self):
        self.graph = {}
        self.to_change = None

    def add_node(self, node):
        self.graph[node] = set()

    def add_edge(self, node, edge):
        self.graph[node].add(edge)

    def top_most(self):
        all_ids = set([node.id for node in self.graph])
        are_dependencies = set(
            [value for values in self.graph.values() for value in values]
        )

        top_most = all_ids - are_dependencies
        if len(top_most) == 1:
            return next(iter(top_most))

    def get_weight(self, node):
        total_weight = node.weight

        edges = self.graph[node]

        weight_edges = {}

        seen_bad = False

        for edge in edges:
            edge_node = self.get_node(edge)
            edge_weight, seen = self.get_weight(edge_node)

            seen_bad |= seen

            if edge_weight not in weight_edges:
                weight_edges[edge_weight] = set()
            weight_edges[edge_weight].add(edge_node)

            total_weight += edge_weight

        if len(weight_edges) == 2 and not seen_bad:
            seen_bad = True

            for weight, edges in weight_edges.items():
                if len(edges) == 1:
                    bad_weight = weight
                else:
                    good_weight = weight

            amount = good_weight - bad_weight

            for weight, edges in weight_edges.items():
                if len(edges) == 1:
                    change = next(iter(edges))
                    weight = change.weight
                    self.to_change = weight + amount

        return total_weight, seen_bad

    def get_node(self, node_id):
        for node in self.graph:
            if node.id == node_id:
                return node

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.graph)


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
        return "{}: {}".format(self.id, self.weight)


def main():
    graph = get_graph()

    top_most = graph.top_most()
    answer.part1("xegshds", top_most)

    graph.get_weight(graph.get_node(top_most))
    answer.part2(299, graph.to_change)


def get_graph():
    graph = Graph()
    for line in Parser().lines():
        line = line.split(" -> ")

        node = Node(line[0])
        graph.add_node(node)

        if len(line) == 2:
            for edge in line[1].split(", "):
                graph.add_edge(node, edge)
    return graph


if __name__ == "__main__":
    main()
