from aoc_parser import Parser


FILE_NAME = 'data'


class Triangle:

    def __init__(self, values):
        sides = [int(value) for value in values]
        sides.sort()
        self.a = sides[0]
        self.b = sides[1]
        self.c = sides[2]

    def valid(self):
        return (self.a + self.b) > self.c


def main():
    # Part 1 = 862
    print('Part 1: {}'.format(num_valid(get_triangles_vertically())))
    # Part 2 = 1577
    print('Part 2: {}'.format(num_valid(get_triangles_horizontally())))


def num_valid(triangles):
    return sum([triangle.valid() for triangle in triangles])


def get_triangles_vertically():
    return [Triangle(line.split()) for line in Parser(FILE_NAME).lines()]


def get_triangles_horizontally():
    triangles = []
    lines = Parser(FILE_NAME).lines()
    for i in range(0, len(lines), 3):
        top_3 = [line.split() for line in lines[i:i+3]]
        for j in range(3):
            sides = [line[j] for line in top_3]
            triangles.append(Triangle(sides))
    return triangles


if __name__ == '__main__':
    main()
