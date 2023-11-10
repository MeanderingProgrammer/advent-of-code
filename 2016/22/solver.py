from dataclasses import dataclass

from aoc import answer, search
from aoc.parser import Parser


@dataclass(frozen=True)
class Node:
    total: int
    used: int
    available: int

    def empty(self) -> bool:
        return self.used == 0

    def can_store(self, o) -> bool:
        return self.available >= o.used

    def could_store(self, o) -> bool:
        return self.total >= o.used


Point = tuple[int, int]
Nodes = dict[Point, Node]


def main() -> None:
    nodes = get_nodes()
    answer.part1(910, viable_connections(nodes))
    answer.part2(222, calculate_transfers(nodes))


def get_nodes() -> Nodes:
    def parse_point(s: str) -> Point:
        point = s.split("/")[-1].split("-")
        return (int(point[1][1:]), int(point[2][1:]))

    def parse_size(s: str) -> int:
        return int(s[:-1])

    nodes = Nodes()
    for line in Parser().lines()[2:]:
        point, total, used, available, _ = line.split()
        nodes[parse_point(point)] = Node(
            total=parse_size(total),
            used=parse_size(used),
            available=parse_size(available),
        )
    return nodes


def viable_connections(nodes: Nodes) -> int:
    viable = 0
    for p1, n1 in nodes.items():
        for p2, n2 in nodes.items():
            if p1 != p2 and not n1.empty() and n2.can_store(n1):
                viable += 1
    return viable


def calculate_transfers(nodes: Nodes) -> int:
    start = [point for point, node in nodes.items() if node.empty()][0]
    end = (max([point[0] for point in nodes]) - 1, 1)
    to_free = search.bfs(start, end, lambda point: get_adjacent(nodes, point))
    assert to_free is not None

    # Amount of movements needed to get free space above node to the left of goal
    # 2 movements to move freed space and transfer goal
    # Each horizontal transfer requires 5 movements
    return to_free + 2 + end[0] * 5


def get_adjacent(nodes: Nodes, point: Point) -> list[Point]:
    result = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        adjacent = (point[0] + dx, point[1] + dy)
        if adjacent in nodes and nodes[point].could_store(nodes[adjacent]):
            result.append(adjacent)
    return result


if __name__ == "__main__":
    main()
