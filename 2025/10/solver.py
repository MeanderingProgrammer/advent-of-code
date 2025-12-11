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
        import z3

        opt = z3.Optimize()
        xs = [z3.Int(f"x{i}") for i in range(len(self.buttons))]

        for x in xs:
            opt.add(x >= 0)

        for i, target in enumerate(self.joltage):
            buttons: list[int] = []
            for j, button in enumerate(self.buttons):
                if i in button:
                    buttons.append(j)
            opt.add(z3.Sum([xs[j] for j in buttons]) == target)

        opt.minimize(z3.Sum(xs))
        assert opt.check() == z3.sat
        model = opt.model()
        presses = [model[x].as_long() for x in xs]
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
