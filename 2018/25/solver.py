from aoc import answer
from aoc.board import Point
from aoc.parser import Parser


class Constallation:
    def __init__(self):
        self.points = set()

    def add(self, point):
        self.points.add(point)

    def add_all(self, points):
        [self.add(point) for point in points]

    def fits(self, to_check):
        for point in self.points:
            difference = point - to_check
            if len(difference) <= 3:
                return True
        return False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.points)


def main():
    constallations = []

    for point in get_points():
        options = get_options(point, constallations)

        if len(options) == 0:
            constallation = Constallation()
            constallation.add(point)
            constallations.append(constallation)
        elif len(options) == 1:
            constallation = options[0]
            constallation.add(point)
        else:
            to_delete = merge(point, options)
            for option in to_delete:
                constallations.remove(option)

    answer.part1(375, len(constallations))


def get_options(point, constallations):
    options = []
    for constallation in constallations:
        if constallation.fits(point):
            options.append(constallation)
    return options


def merge(point, options):
    to_keep = options[0]
    to_keep.add(point)

    to_delete = options[1:]
    for constallation in to_delete:
        to_keep.add_all(constallation.points)

    return to_delete


def get_points():
    points = []
    for line in Parser().lines():
        point = Point(*[int(c) for c in line.split(",")])
        points.append(point)
    return points


if __name__ == "__main__":
    main()
