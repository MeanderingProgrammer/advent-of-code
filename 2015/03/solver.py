from aoc_board import Point
from aoc_parser import Parser


FILE_NAME = 'data'

DIRECTIONS = {
    '^': Point(0, 1),
    'v': Point(0, -1),
    '<': Point(-1, 0),
    '>': Point(1, 0)
}

def main():
    # Part 1: 2081
    print('Part 1: {}'.format(run(1)))
    # Part 2: 2341
    print('Part 2: {}'.format(run(2)))

def run(santas):
    locations = []
    for i in range(santas):
        locations.append(Point(0, 0))

    visited = [location for location in locations]

    for i, direction in enumerate(Parser(FILE_NAME).string()):
        santa_index = i % len(locations)
        locations[santa_index] += DIRECTIONS[direction]
        visited.append(locations[santa_index])

    return len(set(visited))


if __name__ == '__main__':
    main()
