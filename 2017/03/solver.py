from aoc_board import Grid, Point


def main():
    goal = 289_326

    # Part 1: 419
    point, value = build_grid(goal, value_updater_v1)
    print('Part 1: {}'.format(len(point)))

    # Part 2: 295229
    point, value = build_grid(goal, value_updater_v2)
    print('Part 2: {}'.format(value))


def build_grid(goal, value_updater):
    grid = Grid()
    point = Point(0, 0)
    value = 1
    grid[point] = value
    
    while value < goal:
        up_in = point.up() in grid
        down_in = point.down() in grid
        left_in = point.left() in grid
        right_in = point.right() in grid

        if not up_in and not down_in and not left_in and not right_in:
            point = point.right()
        elif not up_in and not right_in:
            if left_in:
                point = point.up()
            else:
                point = point.left()
        elif not up_in and not left_in:
            if down_in:
                point = point.left()
            else:
                point = point.down()
        elif not down_in and not left_in:
            if right_in:
                point = point.down()
            else:
                point = point.right()
        elif not down_in and not right_in:
            if up_in:
                point = point.right()
            else:
                point = point.up()

        value = value_updater(value, grid, point)
        grid[point] = value

    return point, value


def value_updater_v1(previous, grid, point):
    return previous + 1


def value_updater_v2(previous, grid, point):
    return sum([
        grid.get(point.right(), 0),
        grid.get(point.right().up(), 0),
        grid.get(point.up(), 0), 
        grid.get(point.up().left(), 0),
        grid.get(point.left(), 0), 
        grid.get(point.left().down(), 0), 
        grid.get(point.down(), 0),
        grid.get(point.down().right(), 0)
    ])


if __name__ == '__main__':
    main()
