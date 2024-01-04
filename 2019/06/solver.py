from collections import defaultdict
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Orbits:
    orbits: dict[str, list[str]]

    def get_distance(self, start: str, end: str) -> int:
        seen: set[str] = set()
        queue: list[tuple[str, int]] = [(start, -1)]
        for orbit, value in queue:
            for adjacent in self.get_adjacent(orbit):
                if adjacent == end:
                    return value
                elif adjacent not in seen:
                    queue.append((adjacent, value + 1))
            seen.add(orbit)
        raise Exception("Failed")

    def get_adjacent(self, node: str) -> list[str]:
        adjacent: list[str] = list(self.orbits[node])
        for k, v in self.orbits.items():
            if node in v:
                adjacent.append(k)
        return adjacent

    def __len__(self) -> int:
        count: int = 0
        queue: list[tuple[str, int]] = [("COM", 0)]
        for orbit, value in queue:
            count += value
            for adjacent in self.orbits[orbit]:
                queue.append((adjacent, value + 1))
        return count


@answer.timer
def main() -> None:
    orbits = get_orbits()
    answer.part1(358244, len(orbits))
    answer.part2(517, orbits.get_distance("YOU", "SAN"))


def get_orbits() -> Orbits:
    orbits: dict[str, list[str]] = defaultdict(list)
    for orbit in Parser().lines():
        start, end = orbit.split(")")
        orbits[start].append(end)
    return Orbits(orbits=orbits)


if __name__ == "__main__":
    main()
