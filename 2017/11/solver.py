import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


FILE_NAME = 'data'


DIRECTIONS = {
    'ne': Point(1, 1),
    'nw': Point(-1, 1),
    'se': Point(1, -1),
    'sw': Point(-1, -1),
    'n': Point(0, 2),
    's': Point(0, -2)
}


def main():
    directions = get_directions()
    positions = move_to_end(directions)
    steps_required = [steps(position) for position in positions]
    # Part 1 = 812
    print('Steps to end = {}'.format(steps_required[-1]))
     # Part 2 = 1603
    print('Max steps needed = {}'.format(max(steps_required)))


def move_to_end(directions):
    current = Point(0, 0)
    positions = [current]
    for direction in directions:
        adjustment = DIRECTIONS[direction]
        current += adjustment
        positions.append(current)
    return positions


def steps(position):
    x_steps = abs(position.coords[0])
    y_teps = (abs(position.coords[1]) - x_steps) // 2
    return x_steps + max(0, y_teps)
    

def get_directions():
    return Parser(FILE_NAME).csv()


if __name__ == '__main__':
    main()
