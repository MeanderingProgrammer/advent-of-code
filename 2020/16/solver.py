from functools import reduce


class ValueRange:

    def __init__(self, value_range):
        parts = value_range.split('-')
        self.start = int(parts[0])
        self.end = int(parts[1])

    def contains(self, value):
        return value >= self.start and value <= self.end
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}-{}'.format(self.start, self.end)


class Rule:

    def __init__(self, rule):
        parts = rule.split(': ')
        self.field_name = parts[0]
        self.value_ranges = [ValueRange(value_range) for value_range in parts[1].split(' or ')]
        self.row = None

    def matches(self, value):
        for value_range in self.value_ranges:
            if value_range.contains(value):
                return True
        return False

    def starts_with(self, prefix):
        return self.field_name.startswith(prefix)

    def assign(self, i):
        self.row = i

    def is_assigned(self):
        return self.row is not None

    def get_row(self):
        return self.row

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {} assigned to {}'.format(self.field_name, self.value_ranges, self.row)


class Ticket:

    def __init__(self, ticket):
        self.values = [int(value) for value in ticket.split(',')]

    def get_value(self, i):
        return self.values[i]

    def get_unmatched_values(self, rules):
        unmatched_values = []
        for value in self.values:
            if not self.matches_any_rule(value, rules):
                unmatched_values.append(value)
        return unmatched_values

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.values)

    @staticmethod
    def matches_any_rule(value, rules):
        for rule in rules:
            if rule.matches(value):
                return True
        return False
        

def main():
    rules, my_ticket, nearby_tickets = process()
    # Part 1: 26980
    print('Part 1: {}'.format(solve_part_1(rules, nearby_tickets)))
    # Part 2: 3021381607403
    print('Part 2: {}'.format(solve_part_2(rules, my_ticket, nearby_tickets)))


def solve_part_1(rules, nearby_tickets):
    unmatched_values = []
    for ticket in nearby_tickets:
        unmatched_values.extend(ticket.get_unmatched_values(rules))
    return sum(unmatched_values)


def solve_part_2(rules, my_ticket, nearby_tickets):
    remaining_tickets = []
    for ticket in nearby_tickets:
        if len(ticket.get_unmatched_values(rules)) == 0:
            remaining_tickets.append(ticket)

    assign_rules(rules, remaining_tickets)
    departure_indexes = [rule.get_row() for rule in rules if rule.starts_with('departure')]
    departure_values = [my_ticket.get_value(i) for i in departure_indexes]
    return reduce((lambda x, y: x * y), departure_values)


def assign_rules(rules, nearby_tickets):
    while not all([rule.is_assigned() for rule in rules]):
        for i in range(len(rules)):
            values = [ticket.get_value(i) for ticket in nearby_tickets]
            possible_rules = get_possible_rules(rules, values)
            if len(possible_rules) == 1:
                possible_rules[0].assign(i)


def get_possible_rules(rules, values):
    possible_rules = [rule for rule in rules if not rule.is_assigned()]
    for value in values:
        matching_rules = []
        for rule in possible_rules:
            if rule.matches(value):
                matching_rules.append(rule)
        possible_rules = matching_rules
    return possible_rules


def process():
    with open('data.txt', 'r') as f:
        data = f.read().splitlines()

    splits = [i for i in range(len(data)) if data[i] == '']

    rules = [Rule(rule) for rule in data[:splits[0]]]
    my_ticket = Ticket(data[splits[0]+2])
    nearby_tickets = [Ticket(ticket) for ticket in data[splits[1]+2:]]
    return rules, my_ticket, nearby_tickets


if __name__ == '__main__':
    main()
