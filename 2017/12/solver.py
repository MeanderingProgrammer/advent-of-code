from collections import defaultdict

from aoc import answer, search
from aoc.parser import Parser


def main():
    graph = get_graph()

    connected_to_0 = search.connected(graph, "0")
    answer.part1(306, len(connected_to_0))

    heads = set(["0"])
    grouped = set(connected_to_0)

    head = get_ungrouped(graph, grouped)
    while head is not None:
        heads.add(head)
        connected = search.connected(graph, head)
        grouped |= connected
        head = get_ungrouped(graph, grouped)

    answer.part2(200, len(heads))


def get_ungrouped(graph, grouped):
    all_keys = set(graph.keys())
    remainder = all_keys - grouped
    return None if len(remainder) == 0 else next(iter(remainder))


def get_graph():
    graph = defaultdict(set)
    for line in Parser().lines():
        parts = line.split(" <-> ")
        start = parts[0]
        for end in parts[1].split(", "):
            graph[start].add(end)
    return graph


if __name__ == "__main__":
    main()
