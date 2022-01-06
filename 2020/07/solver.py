import commons.answer as answer
from commons.aoc_parser import Parser


class RuleGraph:

    def __init__(self):
        self.graph = {}

    def add(self, node_edges):
        node = node_edges.get_node()
        edges = node_edges.get_edges()
        self.graph[node] = edges

    def get_nodes(self):
        return self.graph.keys()

    def are_connected(self, start, end):
        # In this case the start and end are not conntected
        if start == end:
            return False

        to_explore = [start]
        seen = set()
        seen.add(start)

        for node in to_explore:
            if node == end:
                return True
            next_nodes = self.graph[node]
            next_nodes = [next_node.get_node() for next_node in next_nodes]
            next_nodes = list(filter(lambda next_node: next_node not in seen, next_nodes))
            for next_node in next_nodes:
                seen.add(next_node)
            to_explore.extend(next_nodes)
        return False

    def get_bags_needed(self, start):
        bags_needed = 0
        edges = self.graph[start]
        for edge in edges:
            node = edge.get_node()
            weight = edge.get_weight()

            bags_needed += weight
            bags_needed += (weight * self.get_bags_needed(node))

        return bags_needed


class Edge:

    def __init__(self, raw_edge):
        parts = raw_edge.split()        
        self.node = ' '.join(parts[1:-1])
        self.weight = int(parts[0])

    def get_node(self):
        return self.node

    def get_weight(self):
        return self.weight


class BagRule:

    def __init__(self, line):
        key_raw_edges = line.split(' bags contain ')
        raw_edges = key_raw_edges[1]
        self.node = key_raw_edges[0]
        self.edges = []
        if raw_edges != 'no other bags':
            raw_edges = raw_edges.split(', ')
            for raw_edge in raw_edges:
                self.edges.append(Edge(raw_edge))

    def get_node(self):
        return self.node

    def get_edges(self):
        return self.edges


def main():
    bag_rules = process()

    graph = RuleGraph()
    for bag_rule in bag_rules:
        graph.add(bag_rule)

    answer.part1(172, get_connected_to(graph, 'shiny gold'))
    answer.part2(39645, graph.get_bags_needed('shiny gold'))


def get_connected_to(graph, end):
    nodes = []
    for node in graph.get_nodes():
        connected = graph.are_connected(node, end)
        if connected:
            nodes.append(node)
    return len(nodes)


def process():
    return [BagRule(line[:-1]) for line in Parser().lines()]


if __name__ == '__main__':
    main()
