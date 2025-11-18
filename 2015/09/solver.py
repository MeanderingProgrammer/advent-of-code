import itertools

from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    lines = Parser().lines()

    distances = get_distances(lines)

    locations: set[str] = set()
    for key in distances.keys():
        locations.add(key[0])
        locations.add(key[1])

    values: list[int] = []
    for directions in itertools.permutations(locations):
        value = distance(directions, distances)
        values.append(value)

    answer.part1(141, min(values))
    answer.part2(736, max(values))


def get_distances(lines: list[str]) -> dict[tuple[str, str], int]:
    distances: dict[tuple[str, str], int] = dict()
    for line in lines:
        parts = line.split()
        distances[(parts[0], parts[2])] = int(parts[4])
        distances[(parts[2], parts[0])] = int(parts[4])
    return distances


def distance(directions: tuple[str, ...], distances: dict[tuple[str, str], int]) -> int:
    result = 0
    for i in range(1, len(directions)):
        leg = directions[i - 1], directions[i]
        result += distances[leg]
    return result


if __name__ == "__main__":
    main()
