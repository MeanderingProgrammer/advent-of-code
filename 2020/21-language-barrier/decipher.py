class Food:

    def __init__(self, raw):
        allergen_start = raw.index(' (')

        raw_ingredients = raw[:allergen_start]
        self.ingredients = set(raw_ingredients.split())

        raw_allergens = raw[allergen_start+11:-1]
        self.allergens = set(raw_allergens.split(', '))

    def __repr__(self):
        return str(self)

    def __str__(self):
        details = {}
        details['Ingredients'] = ', '.join(self.ingredients)
        details['Allergens'] = ', '.join(self.allergens)
        return str(details)

def main():
    foods = get_foods()

    solve_part_1(foods)
    solve_part_2(foods)


def solve_part_1(foods):
    # Part 1: 1679
    allergen_possibilities = get_allergen_possibilities(foods)

    possible_ingredients = set()
    for possibilities in allergen_possibilities.values():
        possible_ingredients = possible_ingredients.union(possibilities)

    all_ingredients = get_all_ingredients(foods)
    safe_ingredients = all_ingredients - possible_ingredients
    occurrences = [get_occurrences(foods, ingredient) for ingredient in safe_ingredients]
    print('Total occurrences of safe ingredients = {}'.format(sum(occurrences)))


def solve_part_2(foods):
    # Part 2:
    allergen_possibilities = get_allergen_possibilities(foods)
    total_allergens = len(allergen_possibilities)
    allergen_definitions = {}

    while len(allergen_definitions) != total_allergens:
        for allergen in allergen_possibilities:
            possibilities = allergen_possibilities[allergen]
            if len(possibilities) == 1:
                allergen_definitions[list(possibilities)[0]] = allergen
        for ingredient in allergen_definitions:
            allergen = allergen_definitions[ingredient]
            if allergen in allergen_possibilities:
                del allergen_possibilities[allergen]
            remove_possibility(allergen_possibilities, ingredient)

    ingredients = [ingredient for ingredient in allergen_definitions]
    ingredients = sorted(ingredients, key=lambda ingredient: allergen_definitions[ingredient])
    print('Canonical danger list = {}'.format(','.join(ingredients)))


def get_allergen_possibilities(foods):
    allergen_possibilities = {}
    for allergen in get_all_allergens(foods):
        allergen_possibilities[allergen] = get_possibilities(foods, allergen)
    return allergen_possibilities
        

def get_all_allergens(foods):
    return get_all(foods, lambda food: food.allergens)


def get_all_ingredients(foods):
    return get_all(foods, lambda food: food.ingredients)


def get_all(foods, extractor):
    values = set()
    for food in foods:
        values = values.union(extractor(food))
    return values


def get_occurrences(foods, ingredient):
    is_in = [ingredient in food.ingredients for food in foods]
    return sum(is_in)


def get_possibilities(foods, allergen):
    possibilities = None
    for food in foods:
        if allergen in food.allergens:
            ingredients = food.ingredients
            if possibilities is None:
                possibilities = ingredients
            else:
                possibilities = possibilities.intersection(ingredients)
    return possibilities


def remove_possibility(allergen_possibilities, ingredient):
    for allergen in allergen_possibilities:
        possibilities = allergen_possibilities[allergen]
        if ingredient in possibilities:
            possibilities.remove(ingredient)


def get_foods():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        foods = f.read().splitlines()
    return [Food(food) for food in foods]

if __name__ == '__main__':
    main()
