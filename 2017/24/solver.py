from collections import defaultdict
from dataclasses import dataclass
from typing import Generator, Optional

from aoc import answer
from aoc.parser import Parser

Bridge = list[tuple[int, int]]


def strength(bridge: Bridge) -> int:
    return sum([start + end for start, end in bridge])


@dataclass(frozen=True)
class BridgeBuilder:
    components: dict[int, set[int]]

    def build(self) -> list[Bridge]:
        return list(self.generate(None))

    def generate(self, bridge: Optional[Bridge]) -> Generator[Bridge, None, None]:
        bridge = bridge or []
        start = bridge[-1][1] if len(bridge) > 0 else 0
        for end in self.components[start]:
            if (start, end) in bridge or (end, start) in bridge:
                continue
            new_bridge = bridge + [(start, end)]
            yield new_bridge
            yield from self.generate(new_bridge)


def main() -> None:
    bridges = get_bridge_builder().build()
    answer.part1(1656, strongest(bridges))
    answer.part2(1642, longest_strongest(bridges))


def get_bridge_builder() -> BridgeBuilder:
    components = defaultdict(set)
    for line in Parser().lines():
        p1, p2 = [int(x) for x in line.split("/")]
        components[p1].add(p2)
        components[p2].add(p1)
    return BridgeBuilder(components)


def strongest(bridges: list[Bridge]) -> int:
    return max(map(strength, bridges))


def longest_strongest(bridges: list[Bridge]) -> int:
    longest = max(map(len, bridges))
    return strongest(list(filter(lambda bridge: len(bridge) == longest, bridges)))


if __name__ == "__main__":
    main()
