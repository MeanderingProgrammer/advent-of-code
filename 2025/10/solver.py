from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser
from aoc.search import Search


@dataclass(frozen=True)
class Machine:
    diagram: list[bool]
    joltage: list[int]
    buttons: list[list[int]]

    @classmethod
    def new(cls, s: str) -> Self:
        # "[.#] (1) (1,2) (2) {1,2}"
        parts = s.split()
        # "[.#]" | [false, true]
        diagram = [ch == "#" for ch in parts.pop(0)[1:-1]]
        # {1,2} | [1, 2]
        joltage = Machine.csv(parts.pop())
        # ["(1)", "(1,2)", "(2)"] | [[1], [1, 2], [2]]
        buttons = [Machine.csv(button) for button in parts]
        return cls(diagram, joltage, buttons)

    def start(self) -> int:
        search = Search[tuple[bool, ...]](
            start=tuple([False] * len(self.diagram)),
            end=tuple(self.diagram),
            neighbors=self.neighbors,
        )
        result = search.bfs()
        assert result is not None
        return result

    def neighbors(self, state: tuple[bool, ...]) -> list[tuple[bool, ...]]:
        result: list[tuple[bool, ...]] = []
        for button in self.buttons:
            neighbor = list(state)
            for value in button:
                neighbor[value] = not neighbor[value]
            result.append(tuple(neighbor))
        return result

    def configure(self) -> int:
        from scipy.optimize import LinearConstraint, milp

        a: list[list[int]] = []
        for i in range(len(self.joltage)):
            row: list[int] = []
            for button in self.buttons:
                row.append(1 if i in button else 0)
            a.append(row)
        b = self.joltage
        c = [1] * len(self.buttons)

        result = milp(
            c=c,
            constraints=LinearConstraint(a, b, b),
            integrality=[1] * len(self.buttons),
        )

        assert result.success
        presses = [int(round(x)) for x in result.x]
        return sum(presses)

    @staticmethod
    def csv(s: str) -> list[int]:
        # "(1,2)" | [1, 2]
        # "{1,2}" | [1, 2]
        values = s[1:-1].split(",")
        return [int(value) for value in values]


@answer.timer
def main() -> None:
    lines = Parser().lines()
    machines = [Machine.new(line) for line in lines]
    answer.part1(522, sum(machine.start() for machine in machines))
    answer.part2(18105, sum(machine.configure() for machine in machines))


if __name__ == "__main__":
    main()
