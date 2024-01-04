from dataclasses import dataclass
from typing import Optional

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Node:
    id: str
    weight: int


@dataclass
class Graph:
    graph: dict[Node, set[str]]
    to_change: Optional[int] = None

    def add_node(self, node: Node) -> None:
        self.graph[node] = set()

    def add_edge(self, node: Node, edge: str) -> None:
        self.graph[node].add(edge)

    def top_most(self) -> str:
        all_ids: list[str] = [node.id for node in self.graph]
        connected_to: list[str] = [
            value for values in self.graph.values() for value in values
        ]
        top_most: set[str] = set(all_ids) - set(connected_to)
        assert len(top_most) == 1
        return next(iter(top_most))

    def get_weight(self, node: Node) -> tuple[int, bool]:
        seen_bad = False
        weight_edges: dict[int, set[Node]] = dict()
        total_weight = node.weight
        for edge_id in self.graph[node]:
            edge_node = self.get_node(edge_id)
            edge_weight, seen = self.get_weight(edge_node)
            seen_bad |= seen
            if edge_weight not in weight_edges:
                weight_edges[edge_weight] = set()
            weight_edges[edge_weight].add(edge_node)
            total_weight += edge_weight

        if len(weight_edges) == 2 and not seen_bad:
            amount = 0
            for weight, edges in weight_edges.items():
                if len(edges) == 1:
                    amount -= weight
                else:
                    amount += weight
            for weight, edges in weight_edges.items():
                if len(edges) == 1:
                    change = next(iter(edges))
                    self.to_change = change.weight + amount
            seen_bad = True

        return total_weight, seen_bad

    def get_node(self, node_id: str) -> Node:
        for node in self.graph:
            if node.id == node_id:
                return node
        raise Exception("Failed")


@answer.timer
def main() -> None:
    graph = get_graph()
    top_most = graph.top_most()
    answer.part1("xegshds", top_most)
    graph.get_weight(graph.get_node(top_most))
    answer.part2(299, graph.to_change)


def get_graph() -> Graph:
    def parse_node(part: str) -> Node:
        parts = part.split()
        return Node(id=parts[0], weight=int(parts[1][1:-1]))

    graph = Graph(graph=dict())
    for line in Parser().lines():
        parts = line.split(" -> ")
        node = parse_node(parts[0])
        graph.add_node(node)
        if len(parts) == 2:
            for edge in parts[1].split(", "):
                graph.add_edge(node, edge)
    return graph


if __name__ == "__main__":
    main()
