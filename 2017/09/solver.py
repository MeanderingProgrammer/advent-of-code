from aoc_parser import Parser


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
    group = get_group()
    # Part 1: 15922
    print('Part 1: {}'.format(group.score()))
    # Part 2: 7314
    print('Part 2: {}'.format(group.garbage_removed))


def get_group():
    return Group(Parser(FILE_NAME).read())


if __name__ == '__main__':
    main()
