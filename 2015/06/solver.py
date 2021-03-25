from aoc_board import Grid, Point
from aoc_parser import Parser


FILE_NAME = 'data'

ON = '#'
OFF = '.'


class Action:

    def __init__(self, value):
        self.value = value

    def apply(self, current):
        current = OFF if current is None else current
        if self.value[0] == 'turn':
            if self.value[1] == 'on':
                return ON
            elif self.value[1] == 'off':
                return OFF
            else:
                raise Exception('Unknown turn: {}'.format(self.value))
        elif self.value[0] == 'toggle':
            return ON if current == OFF else OFF
        else:
            raise Exception('Unknown state changer: {}'.format(self.value))

    def apply_v2(self, current):
        current = 0 if current is None else current
        if self.value[0] == 'turn':
            if self.value[1] == 'on':
                return current + 1
            elif self.value[1] == 'off':
                return max(current - 1, 0)
            else:
                raise Exception('Unknown turn: {}'.format(self.value))
        elif self.value[0] == 'toggle':
            return current + 2
        else:
            raise Exception('Unknown state changer: {}'.format(self.value))


class PointRange:

    def __init__(self, value):
        bottom_left = value[0].split(',')
        top_right = value[2].split(',')

        self.left = int(bottom_left[0])
        self.bottom = int(bottom_left[1])

        self.right = int(top_right[0])
        self.top = int(top_right[1])

    def points(self):
        result = []
        for y in range(self.bottom, self.top + 1):
            for x in range(self.left, self.right + 1):
                point = Point(x, y)
                result.append(point)
        return result


class Direction:

    def __init__(self, value):
        value = value.split()
        self.action = Action(value[:-3])
        self.point_range = PointRange(value[-3:])

    def apply(self, grid, v2):
        for point in self.point_range.points():
            current = grid[point]
            if v2:
                new_value = self.action.apply_v2(current)
            else:
                new_value = self.action.apply(current)
            grid[point] = new_value


def main():
    # This one slow, but not slow enough to improve
    # Part 1: 400410
    print('Part 1: {}'.format(run_grid(False)))
    # Part 2: 15343601
    print('Part 2: {}'.format(run_grid(True)))


def run_grid(v2):
    grid = Grid()
    for line in Parser(FILE_NAME).lines():
        direction = Direction(line)
        direction.apply(grid, v2)
    return count_on(grid)


def count_on(grid):
    on = 0
    for point, value in grid.items():
        if value != OFF:
            brightness = 1 if value == ON else value
            on += brightness
    return on


if __name__ == '__main__':
    main()
