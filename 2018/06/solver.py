from aoc_parser import Parser
from aoc_board import Grid, Point


def main():
    file_name = 'data'
    grid = get_grid(file_name)
    # Part 1: 3251
    print('Part 1: {}'.format(solve_part_1(grid)))
    # Part 2: 47841
    print('Part 2: {}'.format(solve_part_2(grid, 10_000)))


def solve_part_1(grid):
    closest_points = grid.closest_points()
    point_counts = get_point_counts(closest_points)
    infinite_points = get_infinite_points(closest_points, grid.max_x(), grid.max_y())

    for infinite_point in infinite_points:
        del point_counts[infinite_point]
    
    sizes = [point_count[1] for point_count in point_counts.items()]
    return max(sizes)


def solve_part_2(grid, max_distance):
    return grid.points_with_max_distance(max_distance)


def get_point_counts(closest_points):
    point_counts = {}
    for point, closest in closest_points:
        if len(closest) == 1:
            closest = closest[0]
            if closest not in point_counts:
                point_counts[closest] = 0
            point_counts[closest] += 1
    return point_counts


def get_infinite_points(closest_points, max_x, max_y):
    infinite_points = set()
    for point, closest in closest_points:
        if point.x in [0, max_x] or point.y in [0, max_y]:
            if len(closest) == 1:
                closest = closest[0]
                infinite_points.add(closest)
    return infinite_points


def get_grid(file_name):
    grid = Grid()
    for line in Parser(file_name).lines():
        parts = line.split(', ')
        point = Point(int(parts[0]), int(parts[1]))
        grid.add(point)
    return grid


if __name__ == '__main__':
    main()
