from aoc import answer
from aoc.board import Point
from aoc.parser import Parser


DIRECTIONS = {
    "ne": Point(1, 1),
    "nw": Point(-1, 1),
    "se": Point(1, -1),
    "sw": Point(-1, -1),
    "n": Point(0, 2),
    "s": Point(0, -2),
}


def main():
    directions = get_directions()
    positions = move_to_end(directions)
    steps_required = [steps(position) for position in positions]
    answer.part1(812, steps_required[-1])
    answer.part2(1603, max(steps_required))


def move_to_end(directions):
    current = Point(0, 0)
    positions = [current]
    for direction in directions:
        adjustment = DIRECTIONS[direction]
        current += adjustment
        positions.append(current)
    return positions


def steps(position):
    x_steps = abs(position.x())
    y_teps = (abs(position.y()) - x_steps) // 2
    return x_steps + max(0, y_teps)


def get_directions():
    return Parser().csv()


if __name__ == "__main__":
    main()
