from aoc import answer
from aoc.parser import Parser


class Recipes:
    def __init__(self, goal: int):
        self.scores = [3, 7]
        self.elf_1 = 0
        self.elf_2 = 1
        self.digits = [int(digit) for digit in str(goal)]

    def evolve(self) -> str:
        while not self.found(0) and not self.found(1):
            self.step()
        return "".join([str(score) for score in self.scores])

    def found(self, offset: int) -> bool:
        return self.scores[-len(self.digits) - offset : -offset] == self.digits

    def step(self) -> None:
        total = self.scores[self.elf_1] + self.scores[self.elf_2]
        if total >= 10:
            self.scores.append(1)
            total %= 10
        self.scores.append(total)
        self.elf_1 = self.update(self.elf_1)
        self.elf_2 = self.update(self.elf_2)

    def update(self, previous: int) -> int:
        return (previous + self.scores[previous] + 1) % len(self.scores)


def main() -> None:
    goal = Parser().integer()
    sequence = Recipes(goal).evolve()
    answer.part1("2103141159", sequence[goal : goal + 10])
    answer.part2(20165733, sequence.index(str(goal)))


if __name__ == "__main__":
    main()
