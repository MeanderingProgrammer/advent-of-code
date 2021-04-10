from commons.aoc_parser import Parser


class Ingredient:

    def __init__(self, raw):
        self.name, components = raw.split(': ')
        components = components.split(', ')
        self.capacity = self.parse_component(components[0])
        self.durability = self.parse_component(components[1])
        self.flavor = self.parse_component(components[2])
        self.texture = self.parse_component(components[3])
        self.calories = self.parse_component(components[4])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: capacity {}, durability {}, flavor {}, texture {}, calories {}'.format(
            self.name, self.capacity, self.durability, self.flavor, self.texture, self.calories
        )

    @staticmethod
    def parse_component(component):
        return int(component.split()[1])


class Recipe:

    def __init__(self, ingredients, teaspoons):
        self.ingredients = ingredients
        self.teaspoons = teaspoons

    def best_score(self, wanted=None):
        scores = []
        for proportion in self.proportions():
            score, calories = self.get_values(proportion)
            if wanted is None or wanted == calories:
                scores.append(score)
        return max(scores)

    def get_values(self, proportion):
        capacity, durability, flavor, texture, calories = 0, 0, 0, 0, 0
        for ingredient, amount in zip(self.ingredients, proportion):
            capacity += (ingredient.capacity * amount)
            durability += (ingredient.durability * amount)
            flavor += (ingredient.flavor * amount)
            texture += (ingredient.texture * amount)
            calories += (ingredient.calories * amount)
        score = max(capacity, 0) * max(durability, 0) * max(flavor, 0) * max(texture, 0)
        return score, calories

    def proportions(self, length=None, total=None):
        length = len(self.ingredients) if length is None else length
        total = self.teaspoons if total is None else total
        if length == 1:
            yield [total]
        else:
            for value in range(total + 1):
                for proportion in self.proportions(length - 1, total - value):
                    yield [value] + proportion


def main():
    ingredients = get_ingredients()
    recipe = Recipe(ingredients, 100)
    # Part 1: 18965440
    print('Part 1: {}'.format(recipe.best_score()))
    # Part 2: 15862900
    print('Part 2: {}'.format(recipe.best_score(500)))


def get_ingredients():
    return [Ingredient(line) for line in Parser().lines()]


if __name__ == '__main__':
    main()
