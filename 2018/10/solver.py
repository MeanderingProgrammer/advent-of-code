from aoc_parser import Parser
from aoc_board import Grid, Point
import re


PATTERN = '^position=<(.*), (.*)> velocity=<(.*), (.*)>$'


def main():
    file_name = 'data'
    point_velocities = get_point_velocities(file_name)
    # Part 1 = GPJLLLLH
    # Part 2 = 10515
    min_time = get_min_area_time(point_velocities)
    print(min_time)
    grid = grid_at_time(point_velocities, min_time)
    print(grid)


def get_min_area_time(point_velocities):
    previous, i = None, 0
    while True:
        grid = grid_at_time(point_velocities, i)
        area = grid.area()
        if previous is not None and area > previous:
            return i - 1
        else:
            previous = area
        i += 1


def grid_at_time(point_velocities, i):
    grid = Grid()
    for point, velocity in point_velocities:
        grid.add(point + (i * velocity))
    return grid


def get_point_velocities(file_name):
    result = []
    for line in Parser(file_name).lines():
        match = re.match(PATTERN, line)
        position = Point(int(match[1]), int(match[2]))
        velocity = Point(int(match[3]), int(match[4]))
        result.append((position, velocity))
    return result


if __name__ == '__main__':
    main()
