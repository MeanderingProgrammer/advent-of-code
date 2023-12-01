from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Food:
    ingredients: set[str]
    allergens: set[str]


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


def main() -> None:
    foods = get_foods()
    answer.part1(1679, non_allergens(foods))
    answer.part2("lmxt,rggkbpj,mxf,gpxmf,nmtzlj,dlkxsxg,fvqg,dxzq", allergens(foods))


def get_foods() -> Foods:
    def parse_food(line: str) -> Food:
        allergen_start = line.index(" (")
        return Food(
            ingredients=set(line[:allergen_start].split()),
            allergens=set(line[allergen_start + 11 : -1].split(", ")),
        )

    return Foods(foods=list(map(parse_food, Parser().lines())))


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
