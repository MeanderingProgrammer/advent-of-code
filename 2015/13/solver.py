from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class People:
    people: tuple[str, ...]

    def score(self, graph: dict[tuple[str, str], int]) -> int:
        scores = [
            graph[(person, self[i - 1])] + graph[(person, self[i + 1])]
            for i, person in enumerate(self.people)
        ]
        return sum(scores)

    def __getitem__(self, i: int) -> str:
        return self.people[i % len(self.people)]


def main() -> None:
    graph = get_graph()
    answer.part1(709, get_max_score(graph, False))
    answer.part2(668, get_max_score(graph, True))


def get_graph() -> dict[tuple[str, str], int]:
    multiplier: dict[str, int] = dict(gain=1, lose=-1)
    graph: dict[tuple[str, str], int] = defaultdict(int)
    for line in Parser().lines():
        parts = line[:-1].split()
        graph[(parts[0], parts[-1])] = multiplier[parts[2]] * int(parts[3])
    return graph


def get_max_score(graph: dict[tuple[str, str], int], include_self: bool) -> int:
    all_people = set([pair[0] for pair in graph.keys()])
    if include_self:
        all_people.add("Myself")
    scores = [People(people).score(graph) for people in permutations(all_people)]
    return max(scores)


if __name__ == "__main__":
    main()
