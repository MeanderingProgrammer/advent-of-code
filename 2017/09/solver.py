from aoc_parser import Parser
from aoc_board import Grid, Point


FILE_NAME = 'data'


class Group:

    def __init__(self, group):
        group = self.remove_special(group)
        self.garbage_removed = 0
        group = self.remove_garbage(group)
        self.group = group

    def score(self):
        score, level = 0, 0
        for char in self.group:
            if char == '{':
                level += 1
                score += level
            elif char == '}':
                level -= 1
        return score

    def remove_special(self, group):
        result, index = [], 0
        while index < len(group):
            char = group[index]
            if char == '!':
                index += 2
            else:
                result.append(char)
                index += 1
        return ''.join(result)

    def remove_garbage(self, group):
        result, index = [], 0
        while index < len(group):
            char = group[index]
            if char == '<':
                end = group[index:].index('>')
                self.garbage_removed += (end - 1)
                index += end
            else:
                result.append(char)
            index += 1
        return ''.join(result)


def main():
    groups = get_groups()
    for group in groups:
        # Part 1 = 15922
        print('Score = {}'.format(group.score()))
        # Part 2 = 7314
        print('Garbage Removed = {}'.format(group.garbage_removed))


def get_groups():
    return [Group(line) for line in Parser(FILE_NAME).lines()]


if __name__ == '__main__':
    main()

