import itertools
from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'

WALL = '#'
OPEN = '.'


def main():
    # Part 1 = 498
    get_shortest_path(False)
    # Part 2 = 804
    get_shortest_path(True)


def get_shortest_path(go_home):
    markers, grid = get_grid()
    distances = calculate_distances(markers, grid)
    shortest = traverse(distances, go_home)
    print('Shortest distance = {}'.format(shortest))


def traverse(distances, go_home):
    shortest = None
    for permutation in generator(len(distances) - 1):
        permutation = list(permutation)
        if go_home:
            permutation += ['0']
        length = get_length(distances, permutation)
        if shortest is None or length < shortest:
            shortest = length
    return shortest


def get_length(distances, permutation):
    total, previous = 0, '0'
    for current in permutation:
        distance = distances[previous][current]
        total += distance
        previous = current
    return total


def generator(n):
    basis = [str(i + 1) for i in range(n)]
    return itertools.permutations(basis)


def calculate_distances(markers, grid):
    distances = {}
    for start_name, start_position in markers.items():
        distances[start_name] = {}
        for end_name, end_position in markers.items():
            if start_name == end_name:
                continue
            if end_name in distances:
                distances[start_name][end_name] = distances[end_name][start_name]
            else:
                distances[start_name][end_name] = aoc_search.bfs(
                    start_position,
                    end_position,
                    get_adjacent(grid)
                )
    return distances


def get_adjacent(grid):
    def actual(position):
        result = []
        for adjacent in position.adjacent():
            if adjacent in grid and grid[adjacent] != WALL:
                result.append(adjacent)
        return result
    return actual


def get_grid():
    markers, grid = {}, Grid()
    for y, line in enumerate(Parser(FILE_NAME).lines()):
        for x, value in enumerate(line):
            point = Point(x, y)
            grid[point] = value
            if value not in [WALL, OPEN]:
                markers[value] = point
    return markers, grid


if __name__ == '__main__':
    main()

