from dataclasses import dataclass

from aoc import answer
from aoc.board import Point
from aoc.parser import Parser

MAPPING: dict[str, Point] = {
    "N": Point(0, 1),
    "E": Point(1, 0),
    "W": Point(-1, 0),
    "S": Point(0, -1),
}


@dataclass
class Regex:
    expression: str
    current: Point
    previous: Point
    positions: list[Point]
    distances: dict

    def calculate_distances(self) -> None:
        # This only works because all options in a parenthesized expression
        # always end at the same location, hence why we only pop and append one path
        for char in self.expression:
            if char == "(":
                self.positions.append(self.current)
            elif char == ")":
                self.current = self.positions.pop()
            elif char == "|":
                self.current = self.positions[-1]
            else:
                self.current += MAPPING[char]
                distance = self.distances.get(self.previous, 0) + 1
                if self.current not in self.distances:
                    self.distances[self.current] = distance
                else:
                    self.distances[self.current] = min(
                        self.distances[self.current], distance
                    )
            self.previous = self.current

    def longest_path(self) -> int:
        return max(self.distances.values())

    def paths_longer(self, min_value: int) -> int:
        return sum([value >= min_value for value in self.distances.values()])


def main() -> None:
    regex = Regex(
        expression=Parser().string()[1:-1],
        current=Point(0, 0),
        previous=Point(0, 0),
        positions=[],
        distances=dict(),
    )
    regex.calculate_distances()
    answer.part1(3930, regex.longest_path())
    answer.part2(8240, regex.paths_longer(1_000))


if __name__ == "__main__":
    main()
