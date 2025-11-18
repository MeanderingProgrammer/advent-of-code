import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Reactant:
    amount: int
    product: str

    def __mul__(self, amount: int) -> Self:
        return type(self)(self.amount * amount, self.product)

    def __sub__(self, amount: int) -> Self:
        return type(self)(self.amount - amount, self.product)


@dataclass(frozen=True)
class Reactions:
    reactions: dict[Reactant, list[Reactant]]

    def ore_for_fuel(self, amount: int) -> int:
        return self.ore_needed(Reactant(amount, "FUEL"), defaultdict(float))

    def ore_needed(self, reactant: Reactant, excess: dict[str, float]) -> int:
        if reactant.product == "ORE":
            return reactant.amount

        times, reaction = self.get_reaction(reactant)
        rounded = math.ceil(times)
        reaction = [component * rounded for component in reaction]

        per_reaction = reactant.amount / times
        excess_times = (rounded * per_reaction) - reactant.amount
        excess[reactant.product] += excess_times

        needed = 0
        for component in reaction:
            amount_had = min(math.floor(excess[component.product]), component.amount)
            excess[component.product] -= amount_had
            component -= amount_had
            if component.amount > 0:
                needed += self.ore_needed(component, excess)
        return needed

    def get_reaction(self, goal: Reactant) -> tuple[float, list[Reactant]]:
        for reactant, values in self.reactions.items():
            if reactant.product == goal.product:
                return goal.amount / reactant.amount, values
        raise Exception("Failed")


@answer.timer
def main() -> None:
    lines = Parser().lines()
    reactions = get_reactions(lines)
    answer.part1(1967319, reactions.ore_for_fuel(1))
    answer.part2(1122036, binary_search(reactions, 1_000_000_000_000, 0, 2_000_000))


def get_reactions(lines: list[str]) -> Reactions:
    def parse_reactant(value: str) -> Reactant:
        amount, product = value.split()
        return Reactant(int(amount), product)

    reactions: dict[Reactant, list[Reactant]] = dict()
    for line in lines:
        components, outcome = line.split(" => ")
        reactions[parse_reactant(outcome)] = [
            parse_reactant(value) for value in components.split(", ")
        ]

    return Reactions(reactions=reactions)


def binary_search(reactions: Reactions, goal: int, start: int, end: int) -> int:
    if end - start == 1:
        return start
    mid_point = (start + end + 1) // 2
    value = reactions.ore_for_fuel(mid_point)
    if value < goal:
        return binary_search(reactions, goal, mid_point, end)
    else:
        return binary_search(reactions, goal, start, mid_point)


if __name__ == "__main__":
    main()
