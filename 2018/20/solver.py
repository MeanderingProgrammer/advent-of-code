from aoc import answer
from aoc.board import Point
from aoc.parser import Parser

OR = "|"
OPEN_PAREN = "("
CLOSE_PAREN = ")"

MAPPING = {"N": Point(0, 1), "E": Point(1, 0), "W": Point(-1, 0), "S": Point(0, -1)}


class Regex:
    def __init__(self, expression):
        self.expression = expression

        self.current = Point(0, 0)
        self.previous = self.current
        self.positions = []
        self.distances = {}

    def calculate_distances(self):
        # This only works because all options in a parenthesized expression
        # always end at the same location, hence why we only pop and append one path
        for char in self.expression:
            if char == OPEN_PAREN:
                self.positions.append(self.current)
            elif char == CLOSE_PAREN:
                self.current = self.positions.pop()
            elif char == OR:
                self.current = self.positions[-1]
            else:
                self.current += MAPPING[char]
                previous_distance = self.distances.get(self.previous, 0)
                if self.current not in self.distances:
                    self.distances[self.current] = previous_distance + 1
                else:
                    self.distances[self.current] = min(
                        self.distances[self.current], previous_distance + 1
                    )
            self.previous = self.current

    def longest_path(self):
        return max(self.distances.values())

    def paths_longer(self, min_value):
        return len([value for value in self.distances.values() if value >= min_value])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.expression)


def main():
    data = Parser().string()
    regex = Regex(data[1:-1])
    regex.calculate_distances()
    answer.part1(3930, regex.longest_path())
    answer.part2(8240, regex.paths_longer(1_000))


def follow_path(path):
    seen = set()

    location = Point(0, 0)
    seen.add(location)

    for direction in path:
        location += MAPPING[direction]
        if location in seen:
            return False
        seen.add(location)
    return True


if __name__ == "__main__":
    main()
