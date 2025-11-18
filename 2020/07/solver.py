from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Edge:
    node: str
    weight: int


@dataclass(frozen=True)
class RuleGraph:
    nodes: dict[str, list[Edge]]

    def connected(self, start: str, end: str) -> bool:
        if start == end:
            return False
        queue: list[str] = [start]
        seen: set[str] = set(queue)
        for node in queue:
            if node == end:
                return True
            for edge in self.nodes[node]:
                if edge.node not in seen:
                    seen.add(edge.node)
                    queue.append(edge.node)
        return False

    def bags_needed(self, start: str) -> int:
        result: int = 0
        for edge in self.nodes[start]:
            result += edge.weight * (1 + self.bags_needed(edge.node))
        return result


@answer.timer
def main() -> None:
    lines = Parser().lines()
    graph = get_rule_graph(lines)
    answer.part1(172, get_connected_to(graph, "shiny gold"))
    answer.part2(39645, graph.bags_needed("shiny gold"))


def get_rule_graph(lines: list[str]) -> RuleGraph:
    def parse_edge(raw_edge: str) -> Edge:
        parts = raw_edge.split()
        return Edge(node=" ".join(parts[1:-1]), weight=int(parts[0]))

    nodes: dict[str, list[Edge]] = dict()
    for line in lines:
        node, raw_edges = line[:-1].split(" bags contain ")
        nodes[node] = (
            []
            if raw_edges == "no other bags"
            else list(map(parse_edge, raw_edges.split(", ")))
        )
    return RuleGraph(nodes=nodes)


def get_connected_to(graph: RuleGraph, end: str) -> int:
    return sum([graph.connected(start, end) for start in graph.nodes])


if __name__ == "__main__":
    main()
