class LetterRule:

    def __init__(self, letter):
        self.letter = letter

    def get_match_indexes(self, rules, value, start_index):
        match_indexes = set()
        if start_index < len(value) and value[start_index] == self.letter:
            match_indexes.add(start_index + 1)
        return match_indexes

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '"{}"'.format(self.letter)


class OrRule:

    def __init__(self, rules):
        self.rules = [AndRule(rule) for rule in rules.split(' | ')]

    def get_match_indexes(self, rules, value, start_index):
        match_indexes = set()
        for rule in self.rules:
            match_indexes.update(rule.get_match_indexes(rules, value, start_index))
        return match_indexes

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ' or '.join([str(rule) for rule in self.rules])


class AndRule:

    def __init__(self, rules):
        self.rules = [int(rule) for rule in rules.split(' ')]

    def get_match_indexes(self, rules, value, start_index):
        match_indexes = set()
        match_indexes.add(start_index)
        for rule in self.rules:
            new_matches = set()
            for match_index in match_indexes:
                new_matches.update(rules[rule].get_match_indexes(rules, value, match_index))
            match_indexes = new_matches
        return match_indexes

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '(' + ' and '.join([str(rule) for rule in self.rules]) + ')'


class Rules:

    def __init__(self, rules):
        self.rules = {}
        for raw_rule in rules:
            parts = raw_rule.split(': ')
            rule_number = int(parts[0])
            rule = parts[1]
            if rule.startswith('"') and rule.endswith('"'):
                rule = LetterRule(rule[1])
            elif '|' in rule:
                rule = OrRule(rule)
            else:
                rule = AndRule(rule)
            self.rules[rule_number] = rule

    def does_match(self, value):
        match_indexes = self.rules[0].get_match_indexes(self.rules, value, 0)
        return len(value) in match_indexes

    def update_for_part_2(self):
        self.rules[8] = OrRule('42 | 42 8')
        self.rules[11] = OrRule('42 31 | 42 11 31')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.rules)


def main():
    # Part 1: 198
    print('Part 1: {}'.format(total_matches(False)))
    # Part 2: 372
    print('Part 2: {}'.format(total_matches(True)))


def total_matches(is_part2):
    rules, messages = process()
    if is_part2:
        rules.update_for_part_2()
    matches = [rules.does_match(message) for message in messages]
    return sum(matches)


def process():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().splitlines()
    split = data.index('')
    return Rules(data[:split]), data[split+1:]


if __name__ == '__main__':
    main()
