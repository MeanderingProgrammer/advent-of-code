import commons.answer as answer
from commons.aoc_board import Point
from commons.aoc_parser import Parser


DIRECTIONS = {
    '^': Point(0, 1),
    'v': Point(0, -1),
    '<': Point(-1, 0),
    '>': Point(1, 0)
}


def main():
    answer.part1(2081, run(1))
    answer.part2(2341, run(2))


def run(santas):
    locations = []
    for i in range(santas):
        locations.append(Point(0, 0))

    visited = [location for location in locations]

    for i, direction in enumerate(Parser().string()):
        santa_index = i % len(locations)
        locations[santa_index] += DIRECTIONS[direction]
        visited.append(locations[santa_index])

    return len(set(visited))


if __name__ == '__main__':
    main()
