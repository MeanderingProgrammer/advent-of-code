import itertools

from aoc import answer
from aoc.parser import Parser


def main() -> None:
    distances = get_distances()
    locations = get_locations(distances)
    options: list[int] = [
        distance(directions, distances)
        for directions in itertools.permutations(locations)
    ]
    answer.part1(141, min(options))
    answer.part2(736, max(options))


def get_distances() -> dict[tuple[str, str], int]:
    distances: dict[tuple[str, str], int] = dict()
    for line in Parser().lines():
        parts = line.split()
        distances[(parts[0], parts[2])] = int(parts[4])
        distances[(parts[2], parts[0])] = int(parts[4])
    return distances


def get_locations(distances: dict[tuple[str, str], int]) -> set[str]:
    locations: set[str] = set()
    for key in distances.keys():
        locations.add(key[0])
        locations.add(key[1])
    return locations


def distance(directions: tuple[str, ...], distances: dict[tuple[str, str], int]) -> int:
    result: list[int] = [
        distances[(directions[i - 1], directions[i])] for i in range(1, len(directions))
    ]
    return sum(result)


if __name__ == "__main__":
    main()
