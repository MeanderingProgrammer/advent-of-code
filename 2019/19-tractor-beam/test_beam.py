from computer import Computer

DEBUG = False


class Point:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.called = False

    def next(self):
        value = self.x if not self.called else self.y
        self.called = not self.called
        return value

    def get(self):
        return (10_000 * self.x) + self.y

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)


class Beam:

    def __init__(self):
        self.__computer = Computer(self, DEBUG)
        self.__point = None
        self.value = None

    def set_memory(self, memory, point):
        self.__computer.set_memory(memory)
        self.__point = point

    def run(self):
        while self.__computer.has_next():
            self.__computer.next()

    def get_input(self):
        return self.__point.next()

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
        edge = Point(point.x + size, point.y - size)
        return self.test(edge) == 1

    def test(self, point):
        self.__beam.set_memory(list(self.__memory), point)
        self.__beam.run()
        return self.__beam.value

def main():
    tester = Tester(get_memory())
    solve_part_1(tester, 0, 0, 50)
    solve_part_2(tester, 100)


def solve_part_1(tester, x_start, y_start, amount):
    # Part 1 = 160
    affected = []
    for y in range(y_start, y_start+amount):
        for x in range(x_start, x_start+amount):
            result = tester.test(Point(x, y))
            affected.append(result)
    print('Total number of affected points = {}'.format(sum(affected)))

def solve_part_2(tester, size):
    # Part 2 = 9441282
    row = 1_000
    while not tester.can_bound(tester.get_left_most_point(row), size):
        row += 1
    top_left = Point(tester.get_left_most_point(row).x, row-99)
    print('Magic number = {}'.format(top_left.get()))


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
