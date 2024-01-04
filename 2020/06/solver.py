from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class BoardingGroup:
    responders: list[str]

    def any_positive(self) -> int:
        responses: set[str] = set(self.responders[0])
        for responder in self.responders[1:]:
            responses |= set(responder)
        return len(responses)

    def all_positive(self) -> int:
        responses: set[str] = set(self.responders[0])
        for responder in self.responders[1:]:
            responses &= set(responder)
        return len(responses)


@answer.timer
def main() -> None:
    groups = [BoardingGroup(group) for group in Parser().line_groups()]
    answer.part1(6782, sum([group.any_positive() for group in groups]))
    answer.part2(3596, sum([group.all_positive() for group in groups]))


if __name__ == "__main__":
    main()
