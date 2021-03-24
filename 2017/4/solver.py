from aoc_parser import Parser
from aoc_board import Grid, Point


FILE_NAME = 'data'


class Password:

    def __init__(self, raw):
        self.words = raw.split()

    def valid(self, check_anagram):
        frequency = {}
        for word in self.words:
            word = self.anagram(word) if check_anagram else word
            if word not in frequency:
                frequency[word] = 0
            frequency[word] += 1
        return all([value == 1 for value in frequency.values()])

    @staticmethod
    def anagram(word):
        anagram = {}
        for letter in word:
            if letter not in anagram:
                anagram[letter] = 0
            anagram[letter] += 1
        return frozenset(anagram.items())


def main():
    # Part 1 = 466
    count_valid(False)
    # Part 2 = 251
    count_valid(True)


def count_valid(check_anagram):
    are_valid = []
    for line in Parser(FILE_NAME).lines():
        valid = Password(line).valid(check_anagram)
        are_valid.append(valid)
    print('Num valid = {}'.format(sum(are_valid)))


if __name__ == '__main__':
    main()

