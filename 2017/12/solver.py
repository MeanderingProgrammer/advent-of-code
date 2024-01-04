from collections import defaultdict
from typing import Optional

from aoc import answer, search
from aoc.parser import Parser


@answer.timer
def main() -> None:
    graph = get_graph()
    connected_to_0 = search.connected(graph, "0")
    answer.part1(306, len(connected_to_0))

    heads: set[str] = set(["0"])
    grouped = connected_to_0
    head = get_ungrouped(graph, grouped)
    while head is not None:
        heads.add(head)
        connected = search.connected(graph, head)
        grouped |= connected
        head = get_ungrouped(graph, grouped)
    answer.part2(200, len(heads))


def get_graph() -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for line in Parser().lines():
        start, ends = line.split(" <-> ")
        for end in ends.split(", "):
            graph[start].add(end)
    return graph


def get_ungrouped(graph: dict[str, set[str]], grouped: set[str]) -> Optional[str]:
    all_keys = set(graph.keys())
    remainder = all_keys - grouped
    return None if len(remainder) == 0 else next(iter(remainder))


if __name__ == "__main__":
    main()
