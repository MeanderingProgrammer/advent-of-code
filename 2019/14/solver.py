import math

from collections import defaultdict


class Reactant:

    def __init__(self, raw):
        parts = raw.split()
        self.amount = int(parts[0])
        self.product = parts[1]

    def __mul__(self, other):
        return Reactant('{} {}'.format(self.amount * other, self.product))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}({})'.format(self.amount, self.product)


class Reactions:

    def __init__(self):
        self.reactions = {}

    def add(self, raw):
        parts = raw.split(' => ')
        outcome = Reactant(parts[1])
        components = [Reactant(comp) for comp in parts[0].split(', ')]
        self.reactions[outcome] = components

    def ore_needed(self, reactant, excess=None):
        if excess is None:
            excess = defaultdict(float)

        if reactant.product == 'ORE':
            return reactant.amount

        times, reaction = self.get_reaction(reactant)
        rounded = math.ceil(times)
        reaction = [component * rounded for component in reaction]

        per_reaction = reactant.amount / times
        excess_times = (rounded * per_reaction) - reactant.amount
        excess[reactant.product] += excess_times

        needed = 0
        for further_reactant in reaction:
            amount_had = min(math.floor(excess[further_reactant.product]), further_reactant.amount)
            excess[further_reactant.product] -= amount_had
            further_reactant.amount -= amount_had
            if further_reactant.amount > 0:
                needed += self.ore_needed(further_reactant, excess)
        return needed

    def get_reaction(self, reactant):
        for k, v in self.reactions.items():
            if k.product == reactant.product:
                times = reactant.amount / k.amount
                return times, v
        return None

    def ore_for_fuel(self, amount):
        return self.ore_needed(Reactant('{} FUEL'.format(amount)))

    def __str__(self):
        return str(self.reactions)


def main():
    reactions = get_reactions()
    # Part 1: 1967319
    print('Part 1: {}'.format(reactions.ore_for_fuel(1)))
    # Part 2: 1122036
    print('Part 2: {}'.format(binary_search(reactions, 1_000_000_000_000, 0, 2_000_000)))


def binary_search(reactions, goal, start, end):
    if end - start == 1:
        return start

    mid_point = (start + end + 1) // 2
    value = reactions.ore_for_fuel(mid_point)

    if value < goal:
        return binary_search(reactions, goal, mid_point, end)
    else: 
        return binary_search(reactions, goal, start, mid_point)


def get_reactions():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().split('\n')

    reactions = Reactions()
    [reactions.add(datum) for datum in data]
    return reactions


if __name__ == '__main__':
    main()
