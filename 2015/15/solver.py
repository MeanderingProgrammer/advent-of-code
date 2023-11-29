from dataclasses import dataclass
from typing import Generator, Optional

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


@dataclass(frozen=True)
class Recipe:
    ingredients: list[Ingredient]
    teaspoons: int

    def best_score(self, wanted: Optional[int] = None) -> int:
        scores: list[int] = []
        for proportion in self.proportions(len(self.ingredients), self.teaspoons):
            score, calories = self.get_values(proportion)
            if wanted is None or wanted == calories:
                scores.append(score)
        return max(scores)

    def proportions(self, length: int, total: int) -> Generator[list[int], None, None]:
        if length == 1:
            yield [total]
        else:
            for value in range(total + 1):
                for proportion in self.proportions(length - 1, total - value):
                    yield [value] + proportion

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


def main() -> None:
    recipe = Recipe(get_ingredients(), 100)
    answer.part1(18965440, recipe.best_score())
    answer.part2(15862900, recipe.best_score(500))


def get_ingredients() -> list[Ingredient]:
    def parse_ingredient(line: str) -> Ingredient:
        name, raw_components = line.split(": ")
        components = raw_components.split(", ")
        return Ingredient(
            name=name,
            capacity=int(components[0].split()[1]),
            durability=int(components[1].split()[1]),
            flavor=int(components[2].split()[1]),
            texture=int(components[3].split()[1]),
            calories=int(components[4].split()[1]),
        )

    return [parse_ingredient(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
