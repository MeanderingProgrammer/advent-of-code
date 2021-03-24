from aoc_parser import Parser
from aoc_board import Grid, Point


class Node:

    def __init__(self, values):
        num_children = values[0]
        num_metadata = values[1]
        values = values[2:]

        self.children = []
        for i in range(num_children):
            child = Node(values)
            self.children.append(child)
            values = values[len(child):]

        self.metadata = values[:num_metadata]

    def sum_metadata(self):
        total = sum(self.metadata)
        for child in self.children:
            total += child.sum_metadata()
        return total

    def value(self):
        if len(self.children) == 0:
            return sum(self.metadata)

        total = 0
        for index in self.metadata:
            index -= 1
            if index >= 0 and index < len(self.children):
                total += self.children[index].value()
        return total

    def __len__(self):
        return 2 + sum([len(child) for child in self.children]) + len(self.metadata)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '(Children = {}, Metadata = {})'.format(self.children, self.metadata)


def main():
    file_name = 'data'
    tree = Node(Parser(file_name).int_entries())
    # Part 1 = 42472
    print('Total metadata = {}'.format(tree.sum_metadata()))
    # Part 2 = 21810
    print('Value = {}'.format(tree.value()))


if __name__ == '__main__':
    main()
