import commons.aoc_search as aoc_search
from commons.aoc_board import Grid, Point


FAVORITE_NUMBER = 1_350
GOAL = Point(31, 39)

GRID = Grid()

def main():
    start = Point(1, 1)
    GRID[start] = False
    # Part 1: 92
    print('Part 1: {}'.format(aoc_search.bfs(start, GOAL, get_adjacent)))
    # Part 2: 124
    print('Part 2: {}'.format(len(aoc_search.reachable(start, 50, get_adjacent))))


def get_adjacent(position):
    result = set()
    for adjacent in position.adjacent():
        if is_valid(adjacent):
            if adjacent not in GRID:
                GRID[adjacent] = is_wall(adjacent)
            if not GRID[adjacent]:
                result.add(adjacent)
    return result


def is_valid(point):
    return point.x() >= 0 and point.y() >= 0 


def is_wall(point):
    x = point.x()
    y = point.y()
    value = (x*x) + (3*x) + (2*x*y) + y + y*y
    value += FAVORITE_NUMBER
    value = bin(value)[2:]
    num_ones = sum([v == '1' for v in value])
    return num_ones % 2 == 1


if __name__ == '__main__':
    main()
