import commons.answer as answer
from commons.aoc_parser import Parser


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
    answer.part1(862, num_valid(get_triangles_vertically()))
    answer.part2(1577, num_valid(get_triangles_horizontally()))


def num_valid(triangles):
    return sum([triangle.valid() for triangle in triangles])


def get_triangles_vertically():
    return [Triangle(line.split()) for line in get_lines()]


def get_triangles_horizontally():
    triangles, lines = [], get_lines()

    for i in range(0, len(lines), 3):
        top_3 = [line.split() for line in lines[i:i+3]]
        for j in range(3):
            sides = [line[j] for line in top_3]
            triangles.append(Triangle(sides))

    return triangles


def get_lines():
    return Parser().lines()


if __name__ == '__main__':
    main()
