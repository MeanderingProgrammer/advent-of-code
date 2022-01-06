import re

import commons.answer as answer
from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


PATTERN = '^position=<(.*), (.*)> velocity=<(.*), (.*)>$'


def main():
    point_velocities = get_point_velocities()
    min_time = get_min_area_time(point_velocities)
    grid = grid_at_time(point_velocities, min_time)

    # Part 1: GPJLLLLH
    print('Part 1')
    print(grid)

    answer.part2(10515, min_time)


def get_min_area_time(point_velocities):
    previous, i = None, 0
    while True:
        grid = grid_at_time(point_velocities, i)
        area = grid.area()
        if previous is not None and area > previous:
            return i - 1
        previous = area
        i += 1


def grid_at_time(point_velocities, i):
    grid = Grid()
    for point, velocity in point_velocities:
        point += (i * velocity)
        grid[point] = '#'
    return grid


def get_point_velocities():
    result = []
    for line in Parser().lines():
        match = re.match(PATTERN, line)
        position = Point(int(match[1]), int(match[2]))
        velocity = Point(int(match[3]), int(match[4]))
        result.append((position, velocity))
    return result


if __name__ == '__main__':
    main()
