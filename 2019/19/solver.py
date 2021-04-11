from commons.aoc_parser import Parser
from commons.int_code import Computer
from commons.aoc_board import Point


class Beam:

    def __init__(self):
        self.__computer = Computer(self)

        self.__point = None
        self.__called = False

        self.value = None

    def set_memory(self, memory, point):
        self.__computer.set_memory(memory)
        self.__point = point

    def run(self):
        self.__computer.run()

    def get_input(self):
        value = self.__point.x() if not self.__called else self.__point.y()
        self.__called = not self.__called
        return value

    def add_output(self, value):
        self.value = value


class Tester:

    def __init__(self, memory):
        self.__beam = Beam()
        self.__memory = memory
        self.__beam_starts = {}

    def get_left_most_point(self, y):
        x = self.__beam_starts.get(y - 1, 0)
        while self.test(Point(x, y)) != 1:
            x += 1
        self.__beam_starts[y] = x
        return Point(x, y)

    def can_bound(self, point, size):
        size -= 1
        edge = Point(point.x() + size, point.y() - size)
        return self.test(edge) == 1

    def test(self, point):
        self.__beam.set_memory(list(self.__memory), point)
        self.__beam.run()
        return self.__beam.value


def main():
    tester = Tester(get_memory())
    # Part 1: 160
    print('Part 1: {}'.format(affected_points(tester, 0, 0, 50)))
    # Part 2: 9441282
    print('Part 2: {}'.format(bounding_point(tester, 100)))


def affected_points(tester, x_start, y_start, amount):
    affected = []
    for y in range(y_start, y_start+amount):
        for x in range(x_start, x_start+amount):
            result = tester.test(Point(x, y))
            affected.append(result)
    return sum(affected)


def bounding_point(tester, size):
    row = 1_000
    while not tester.can_bound(tester.get_left_most_point(row), size):
        row += 1
    x, y = tester.get_left_most_point(row).x(), row - 99
    return (10_000 * x) + y


def get_memory():
    return Parser().int_csv()


if __name__ == '__main__':
    main()
