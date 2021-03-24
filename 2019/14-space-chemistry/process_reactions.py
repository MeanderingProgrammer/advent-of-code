from collections import defaultdict
import math


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

    def __str__(self):
        return str(self.reactions)

def main():
    reactions = get_reactions()
    solve_part_1(reactions)
    solve_part_2(reactions)


def solve_part_1(reactions):
    # Part 1 = 1967319
    ore_needed = reactions.ore_needed(Reactant('1 FUEL'))
    print('Amount of ore needed = {}'.format(ore_needed))


def solve_part_2(reactions):
    # Part 2 = 1122036
    nearest_10_000 = iterate_by_step(reactions, 1, 10_000)
    nearest_100 = iterate_by_step(reactions, nearest_10_000, 100)
    exact_answer = iterate_by_step(reactions, nearest_100, 1)
    print('Total fuel from 1 trillion ore = {}'.format(exact_answer))


def iterate_by_step(reactions, start, step_size):
    amount_of_fuel = start
    while True:
        ore_needed = reactions.ore_needed(Reactant('{} FUEL'.format(amount_of_fuel)))
        if ore_needed > 1_000_000_000_000:
            return amount_of_fuel - step_size
        else:
            amount_of_fuel += step_size


def get_reactions():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().split('\n')

    reactions = Reactions()
    [reactions.add(datum) for datum in data]
    return reactions


if __name__ == '__main__':
    main()
