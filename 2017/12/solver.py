from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Graph:
    graph: dict[str, set[str]]

    def connected(self, start: str) -> set[str]:
        queue: list[str] = [start]
        seen: set[str] = set()
        while len(queue) > 0:
            current = queue.pop()
            if current in seen:
                continue
            seen.add(current)
            for adjacent in self.graph[current]:
                if adjacent not in seen:
                    queue.append(adjacent)
        return seen

    def get_ungrouped(self, grouped: set[str]) -> Optional[str]:
        all_keys: set[str] = set(self.graph.keys())
        remainder: set[str] = all_keys - grouped
        return None if len(remainder) == 0 else next(iter(remainder))


@answer.timer
def main() -> None:
    graph = get_graph()

    connected_to_0: set[str] = graph.connected("0")
    answer.part1(306, len(connected_to_0))

    heads: set[str] = set(["0"])
    grouped: set[str] = connected_to_0
    head: Optional[str] = graph.get_ungrouped(grouped)
    while head is not None:
        heads.add(head)
        grouped |= graph.connected(head)
        head = graph.get_ungrouped(grouped)
    answer.part2(200, len(heads))


def get_graph() -> Graph:
    graph: dict[str, set[str]] = defaultdict(set)
    for line in Parser().lines():
        start, ends = line.split(" <-> ")
        for end in ends.split(", "):
            graph[start].add(end)
    return Graph(graph=graph)


if __name__ == "__main__":
    main()
