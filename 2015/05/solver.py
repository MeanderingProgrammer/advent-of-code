from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class Word:

    def __init__(self, value):
        self.value = value

    def nice(self, new_rules):
        if not new_rules:
            return self.old_nice()
        else:
            return self.new_nice()

    def old_nice(self):
        groups = self.group_data()

        num_vowels = self.num_vowels()
        contains_repeat = self.contains_repeat(groups)
        contains_illegal = self.contains_illegal(groups)

        return num_vowels >= 3 and contains_repeat and not contains_illegal

    def new_nice(self):
        groups = self.group_data()
        repeat_non_overlapping = self.repeat_non_overlapping(groups)
        creates_tripple = self.creates_tripple(groups)
        return repeat_non_overlapping and creates_tripple


    def repeat_non_overlapping(self, groups):
        group_frequencies = defaultdict(int)
        group_frequencies[groups[0]] += 1

        for i, group in enumerate(groups[1:]):
            num_needed = 1 if group != groups[i] else 2
            if group_frequencies[group] >= num_needed:
                return True
            group_frequencies[group] += 1

        return False

    def creates_tripple(self, groups):
        for i, group in enumerate(groups[1:]):
            if groups[i][0] == group[1]:
                return True
        return False

    def num_vowels(self):
        vowels = ['a', 'e', 'i', 'o', 'u']
        return sum([letter in vowels for letter in self.value])

    def group_data(self):
        groups = []
        for i in range(len(self.value) - 1):
            groups.append(self.value[i] + self.value[i+1])
        return groups

    def contains_repeat(self, groups):
        for group in groups:
            if group[0] == group[1]:
                return True
        return False

    def contains_illegal(self, groups):
        illegal_groups = ['ab', 'cd', 'pq', 'xy']
        for illegal_group in illegal_groups:
            if illegal_group in groups:
                return True
        return False


def main():
    # Part 1 = 238
    total_nice_words(False)
    # Part 2 = 69
    total_nice_words(True)


def total_nice_words(new_rules):
    nice_words = 0
    for line in Parser(FILE_NAME).lines():
        word = Word(line)
        if word.nice(new_rules):
            nice_words += 1
    print(nice_words)


if __name__ == '__main__':
    main()

