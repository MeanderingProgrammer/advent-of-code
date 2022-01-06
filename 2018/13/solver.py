import commons.answer as answer
from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


LEFT = '<'
RIGHT = '>'
UP = '^'
DOWN = 'v'

OPPOSITES = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    UP: DOWN, 
    DOWN: UP
}

AS_POSITION = {
    LEFT: Point(-1, 0),
    RIGHT: Point(1, 0),
    UP: Point(0, -1), 
    DOWN: Point(0, 1)
}

INTERSECTION_OPTIONS = {
    LEFT: [DOWN, LEFT, UP],
    RIGHT: [UP, RIGHT, DOWN],
    UP: [LEFT, UP, RIGHT],
    DOWN: [RIGHT, DOWN, LEFT]
}


class Cart:

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.choice = 0

    def go(self, options):
        if len(options) == 4:
            self.handle_intersection()
        elif len(options) == 2:
            self.standard_movement(options)
        else:
            raise Exception('Unhandled number of options')

    def handle_intersection(self):
        options = INTERSECTION_OPTIONS[self.direction]
        self.direction = options[self.choice % len(options)]
        self.choice += 1
        self.position += AS_POSITION[self.direction]

    def standard_movement(self, options):
        opposite = OPPOSITES[self.direction]
        dont_go = self.position + AS_POSITION[opposite]
        options.remove(dont_go)

        if len(options) != 1:
            raise Exception('Unable to eliminate enough options')

        new_position = options[0]
        self.direction = self.how_to_get(new_position)
        self.position = new_position

    def how_to_get(self, new_position):
        for direction in AS_POSITION:
            if self.position + AS_POSITION[direction] == new_position:
                return direction
        raise Exception('Unable to determine how to reach position')

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, o):
        if self.position.y() == o.position.y():
            return self.position.x() < o.position.x()
        return self.position.y() < o.position.y()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} @ {}'.format(self.direction, self.position)


class CartSystem:

    def __init__(self, track, carts):
        self.track = track
        self.carts = carts

    def run_until_crash(self):
        crash_positions = []
        while len(crash_positions) == 0:
            crash_positions = self.tick()
        return crash_positions

    def run_unit_one_remains(self):
        while len(self.carts) > 1:
            self.tick()
        return self.carts[0].position

    def tick(self):
        crash_positions = []
        carts_crashed = []
        self.carts.sort()
        for cart in self.carts:
            adjacent = self.adjacent(cart.position)
            cart.go(adjacent)
            new_position = cart.position
            carts_at_same_position = self.carts_at(new_position)
            if len(carts_at_same_position) > 1:
                carts_crashed.extend(carts_at_same_position)
                crash_positions.append(new_position)
        for cart_crashed in carts_crashed:
            self.carts.remove(cart_crashed)
        return crash_positions

    def adjacent(self, point):
        value = self.track[point]
        if value == '+':
            return [
                point.left(), 
                point.right(), 
                point.up(), 
                point.down()
            ]
        elif value == '|':
            return [
                point.up(), 
                point.down()
            ]
        elif value == '-':
            return [
                point.left(), 
                point.right()
            ]
        elif value == '/':
            if self.track[point.up()] in ['|', '+']:
                return [
                    point.up(), 
                    point.right()
                ]
            else:
                return [
                    point.down(), 
                    point.left()
                ]
        elif value == '\\':
            if self.track[point.up()] in ['|', '+']:
                return [
                    point.up(), 
                    point.left()
                ]
            else:
                return [
                    point.down(), 
                    point.right()
                ]
        else:
            raise Exception('Unknown value at point')

    def carts_at(self, position):
        return [cart for cart in self.carts if cart.position == position]

    def __repr__(self):
        return str(self)

    def __str__(self):
        values = [[value for value in row] for row in str(self.track).split('\n')]

        for cart in self.carts:
            position = cart.position
            values[position.y][position.x] = cart.direction

        values = [''.join(row) for row in values]
        return '\n'.join(values)


def main():
    data = get_data()

    system = CartSystem(get_track(data), get_carts(data))
    answer.part1(Point(86, 118), system.run_until_crash()[0])

    system = CartSystem(get_track(data), get_carts(data))
    answer.part2(Point(2, 81), system.run_unit_one_remains())


def get_data():
    data = {}
    for y, row in enumerate(Parser().nested_lines()):
        for x, value in enumerate(row):
            data[Point(x, y)] = value
    return data


def get_track(data):
    track = Grid()
    for point in data:
        value = data[point]
        if value != ' ':
            value = '-' if value in [LEFT, RIGHT] else value
            value = '|' if value in [UP, DOWN] else value
            track[point] = value
    return track


def get_carts(data):
    carts = []
    for point in data:
        value = data[point]
        if value in [LEFT, RIGHT, UP, DOWN]:
            carts.append(Cart(point, value))
    return carts


if __name__ == '__main__':
    main()
