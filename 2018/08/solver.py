from typing import Self

from aoc import answer
from aoc.parser import Parser


class Node:
    def __init__(self, values: list[int]):
        num_children: int = values[0]
        num_metadata: int = values[1]
        values = values[2:]

        self.children: list[Self] = []
        for _ in range(num_children):
            child = Node(values)
            self.children.append(child)
            values = values[len(child) :]

        self.metadata: list[int] = values[:num_metadata]

    def sum_metadata(self) -> int:
        return sum(self.metadata) + sum(
            [child.sum_metadata() for child in self.children]
        )

    def value(self) -> int:
        if len(self.children) == 0:
            return sum(self.metadata)
        total: int = 0
        for index in self.metadata:
            index -= 1
            if index >= 0 and index < len(self.children):
                total += self.children[index].value()
        return total

    def __len__(self) -> int:
        return 2 + sum([len(child) for child in self.children]) + len(self.metadata)


def main() -> None:
    tree = Node(Parser().int_entries())
    answer.part1(42472, tree.sum_metadata())
    answer.part2(21810, tree.value())


if __name__ == "__main__":
    main()
