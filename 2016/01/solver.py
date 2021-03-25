from aoc_parser import Parser
from aoc_board import Point


FILE_NAME = 'data'


DIRECTIONS = [
    Point(0, 1),
    Point(1, 0),
    Point(0, -1),
    Point(-1, 0)
]


def main():
    visited = traverse()
    # Part 1: 252
    print('Part 1: {}'.format(len(visited[-1])))
    # Part 2: 143
    print('Part 2: {}'.format(len(repeated(visited))))

def traverse():
    index, position = 0, Point(0, 0)
    visited = [position]

    for instruction in Parser(FILE_NAME).csv():
        change = -1 if instruction[0] == 'L' else 1
        index = (index + change) % len(DIRECTIONS)
        amount = int(instruction[1:])
        for i in range(amount):
            position += DIRECTIONS[index]
            visited.append(position)

    return visited


def repeated(visited):
    seen = set()
    for position in visited:
        if position in seen:
            return position
        else:
            seen.add(position)


if __name__ == '__main__':
    main()
