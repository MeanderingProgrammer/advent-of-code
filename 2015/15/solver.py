from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @classmethod
    def new(cls, s: str) -> Self:
        name, components_string = s.split(": ")
        components = components_string.split(", ")
        return cls(
            name=name,
            capacity=int(components[0].split()[1]),
            durability=int(components[1].split()[1]),
            flavor=int(components[2].split()[1]),
            texture=int(components[3].split()[1]),
            calories=int(components[4].split()[1]),
        )


@dataclass(frozen=True)
class Recipe:
    ingredients: list[Ingredient]
    teaspoons: int
    target: int

    def best_scores(self) -> tuple[int, int]:
        part1: int = 0
        part2: int = 0
        for a in range(self.teaspoons + 1):
            for b in range(self.teaspoons + 1 - a):
                for c in range(self.teaspoons + 1 - a - b):
                    d = self.teaspoons - a - b - c
                    score, calories = self.get_values([a, b, c, d])
                    part1 = max(part1, score)
                    if self.target == calories:
                        part2 = max(part2, score)
        return part1, part2

    def get_values(self, proportion: list[int]) -> tuple[int, int]:
        capacity, durability, flavor, texture, calories = 0, 0, 0, 0, 0
        for ingredient, amount in zip(self.ingredients, proportion):
            capacity += ingredient.capacity * amount
            durability += ingredient.durability * amount
            flavor += ingredient.flavor * amount
            texture += ingredient.texture * amount
            calories += ingredient.calories * amount
        score = max(capacity, 0) * max(durability, 0) * max(flavor, 0) * max(texture, 0)
        return score, calories


@answer.timer
def main() -> None:
    ingredients = [Ingredient.new(line) for line in Parser().lines()]
    assert len(ingredients) == 4
    recipe = Recipe(ingredients, 100, 500)
    part1, part2 = recipe.best_scores()
    answer.part1(18965440, part1)
    answer.part2(15862900, part2)


if __name__ == "__main__":
    main()
