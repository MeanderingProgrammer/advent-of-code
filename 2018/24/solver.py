from aoc_parser import Parser


FILE_NAME = 'data'


class Group:

    def __init__(self, group, id, raw):
        self.id = (group, id)
        self.units = self.get_units(raw)
        self.hp = self.get_hp(raw)

        traits = self.get_traits(raw)
        self.weaknesses = traits.get('weak', [])
        self.immunities = traits.get('immune', [])

        self.damage = self.get_damage(raw)
        self.damage_type = self.get_damage_type(raw)
        self.initiative = self.get_initiative(raw)
        self.boost = None

    def effective_power(self):
        return self.units * self.damage

    def apply_damage(self, damage_dealt):
        units_destroyed = damage_dealt // self.hp
        self.units -= units_destroyed

    def is_dead(self):
        return self.units <= 0

    def target_selection_value(self):
        return self.effective_power(), self.initiative

    def target_value(self, o):
        return self.would_deal(o), o.effective_power(), o.initiative

    def attack_value(self):
        return self.initiative

    def immune_to(self, o):
        return o.damage_type in self.immunities

    def weak_to(self, o):
        return o.damage_type in self.weaknesses

    def would_deal(self, o):
        multiplier = 1
        if o.immune_to(self):
            multiplier = 0 
        elif o.weak_to(self):
            multiplier = 2
        return self.effective_power() * multiplier

    def __eq__(self, o):
        if o is None:
            return False
        return str(self.id) == str(o.id)

    def __hash__(self):
        return hash(str(self.id))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{' + ', '.join([
            'Units = {}'.format(self.units),
            'HP = {}'.format(self.hp),
            'Damage = {}'.format(self.damage)
        ]) + '}'

    @staticmethod
    def get_units(raw):
        return int(raw.split()[0])

    @staticmethod
    def get_hp(raw):
        return int(raw.split()[4])

    @staticmethod
    def get_traits(raw):
        traits = {}

        start = raw.find('(')
        if start == -1:
            return traits
        end = raw.index(')')
        raw = raw[start+1:end]

        for part in raw.split('; '):
            trait_details = part.split(' to ')
            traits[trait_details[0]] = trait_details[1].split(', ')

        return traits

    @staticmethod
    def get_damage(raw):
        return int(raw.split()[-6])

    @staticmethod
    def get_damage_type(raw):
        return raw.split()[-5]

    @staticmethod
    def get_initiative(raw):
        return int(raw.split()[-1])


class Battle:

    def __init__(self, armies):
        self.immune_system = armies[0]
        self.infection = armies[1]
        self.assigned = {}

    def boost_immune(self, value):
        for group in self.immune_system:
            group.damage += value

    def simulate(self):
        current, previous = None, 0
        while self.should_continue() and current != previous:
            self.assign_targets()
            self.attack()
            self.assigned = {}
            previous = current
            current = self.winning_units()

    def assign_targets(self):
        groups = self.get_groups()
        groups.sort(key=lambda group: group.target_selection_value(), reverse=True)
        for group in groups:
            to_attack = self.get_group_to_attack(group)
            self.assigned[group] = to_attack

    def get_group_to_attack(self, group):
        options = self.immune_system if group in self.infection else self.infection
        options = [option for option in options if option not in self.assigned.values()]
        options.sort(key=lambda option: group.target_value(option), reverse=True)
        if len(options) == 0:
            return None
        to_attack = options[0]
        if group.would_deal(to_attack) == 0:
            return None
        return to_attack

    def attack(self):
        groups = self.get_groups()
        groups.sort(key=lambda group: group.attack_value(), reverse=True)
        for group in groups:
            to_attack = self.assigned[group]
            if not group.is_dead() and to_attack is not None:
                damage_dealt = group.would_deal(to_attack)
                to_attack.apply_damage(damage_dealt)
                self.cleanup(to_attack)

    def should_continue(self):
        return len(self.immune_system) > 0 and len(self.infection) > 0

    def cleanup(self, group):
        if group.is_dead():
            if group in self.immune_system:
                self.immune_system.remove(group)
            else:
                self.infection.remove(group)

    def immune_won(self):
        return len(self.immune_system) > 0 and len(self.infection) == 0

    def winning_units(self):
        return sum([group.units for group in self.get_groups()])

    def get_groups(self):
        return self.immune_system + self.infection
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join([
            'Immune System:\n{}'.format(self.immune_system),
            'Infection:\n{}'.format(self.infection)
        ])


def main():
    # Part 1: 16086
    print('Part 1: {}'.format(solve_part_1()))
    # Part 2: 3957
    print('Part 2: {}'.format(solve_part_2()))


def solve_part_1():
    battle = Battle(get_armies())
    battle.simulate()
    return battle.winning_units()


def solve_part_2():
    boost = 0
    immune_won = False
    while not immune_won:
        boost += 1
        battle = Battle(get_armies())
        battle.boost_immune(boost)
        battle.simulate()
        immune_won |= battle.immune_won()
    
    return battle.winning_units()


def get_armies():
    armies = []
    for i, group in enumerate(Parser(FILE_NAME).line_groups()):
        armies.append([Group(i, j, g) for j, g in enumerate(group[1:])])
    return armies


if __name__ == '__main__':
    main()
