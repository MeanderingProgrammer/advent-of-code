import commons.aoc_util as aoc_util
from commons.aoc_parser import Parser


class Rule:

    def __init__(self, raw):
        self.start, self.end = raw.split(' => ')

    def replace(self, value):
        indexes = aoc_util.find_all(value, self.start)
        results = set()
        for index in indexes:
            results.add(self.replace_at(value, index))
        return results

    def replace_at(self, value, index):
        before = value[:index]
        after = value[index+len(self.start):]
        return before + self.end + after


def main():
    molecule, rules = get_data()
    # Part 1: 576
    print('Part 1: {}'.format(len(run(rules, molecule))))
    # Part 2: 207
    print('Part 2: {}'.format(replacements_needed(molecule)))


def run(rules, molecule):
    results = set()
    for rule in rules:
        results |= rule.replace(molecule)
    return results


def replacements_needed(molecule):
    # Solution by askalski
    # https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/
    elements = sum([letter.isupper() for letter in molecule])
    rn_count = len(aoc_util.find_all(molecule, 'Rn'))
    ar_count = len(aoc_util.find_all(molecule, 'Ar'))
    y_count = len(aoc_util.find_all(molecule, 'Y'))
    return elements - rn_count - ar_count - (2 * y_count) - 1


def get_data():
    groups = Parser().line_groups()
    rules = [Rule(value) for value in groups[0]]
    return groups[1][0], rules


if __name__ == '__main__':
    main()
