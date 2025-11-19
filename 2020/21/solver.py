from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Food:
    ingredients: set[str]
    allergens: set[str]

    @classmethod
    def new(cls, s: str) -> Self:
        start = s.index(" (")
        return cls(
            ingredients=set(s[:start].split()),
            allergens=set(s[start + 11 : -1].split(", ")),
        )


@dataclass(frozen=True)
class Foods:
    foods: list[Food]

    def allergen_possibilities(self) -> dict[str, set[str]]:
        result: dict[str, set[str]] = dict()
        for allergen in self.allergens():
            result[allergen] = self.possibilities(allergen)
        return result

    def possibilities(self, allergen: str) -> set[str]:
        result = None
        for food in self.foods:
            if allergen in food.allergens:
                if result is None:
                    result = food.ingredients
                else:
                    result = result.intersection(food.ingredients)
        assert result is not None
        return result

    def allergens(self) -> set[str]:
        result: set[str] = set()
        for food in self.foods:
            result.update(food.allergens)
        return result

    def ingredients(self) -> set[str]:
        result: set[str] = set()
        for food in self.foods:
            result.update(food.ingredients)
        return result

    def occurrences(self, ingredient: str) -> int:
        return sum([ingredient in food.ingredients for food in self.foods])


@answer.timer
def main() -> None:
    foods = Foods(foods=[Food.new(line) for line in Parser().lines()])
    answer.part1(1679, non_allergens(foods))
    answer.part2("lmxt,rggkbpj,mxf,gpxmf,nmtzlj,dlkxsxg,fvqg,dxzq", allergens(foods))


def non_allergens(foods: Foods) -> int:
    allergens: set[str] = set()
    for possibilities in foods.allergen_possibilities().values():
        allergens.update(possibilities)
    ingredients = foods.ingredients() - allergens
    return sum([foods.occurrences(ingredient) for ingredient in ingredients])


def allergens(foods: Foods) -> str:
    allergen_possibilities = foods.allergen_possibilities()

    definitions: dict[str, str] = dict()
    while len(allergen_possibilities) > 0:
        for allergen, possibilities in allergen_possibilities.items():
            if len(possibilities) == 1:
                definitions[list(possibilities)[0]] = allergen

        for ingredient, allergen in definitions.items():
            if allergen in allergen_possibilities:
                del allergen_possibilities[allergen]

            for possibilities in allergen_possibilities.values():
                if ingredient in possibilities:
                    possibilities.remove(ingredient)

    ingredients = list(definitions.keys())
    ingredients.sort(key=lambda ingredient: definitions[ingredient])
    return ",".join(ingredients)


if __name__ == "__main__":
    main()
