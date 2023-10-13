from aoc import answer
from aoc.parser import Parser


class Node:
    def __init__(self, values):
        num_children = values[0]
        num_metadata = values[1]
        values = values[2:]

        self.children = []
        for i in range(num_children):
            child = Node(values)
            self.children.append(child)
            values = values[len(child) :]

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
        return "(Children = {}, Metadata = {})".format(self.children, self.metadata)


def main():
    tree = Node(Parser().int_entries())
    answer.part1(42472, tree.sum_metadata())
    answer.part2(21810, tree.value())


if __name__ == "__main__":
    main()
