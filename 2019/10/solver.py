import math
from collections import defaultdict

from commons.aoc_parser import Parser


class Point:

    def __init__(self, x, y):
        self.x, self.y = x, y

    def angle(self, other):
        dy = other.y - self.y 
        dx = other.x - self.x
        # Correct for inverted y coordinates
        angle = math.degrees(math.atan2(-dy, dx))
        # Correct for 0 degrees being at top
        angle -= 90
        # Correct for negative values and flipped direction
        return -angle if angle <= 0 else 360 - angle

    def distance(self, other):
        dy = self.y - other.y 
        dx = self.x - other.x
        return pow(pow(dx, 2) + pow(dy, 2), 0.5)

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)


class Grid:

    def __init__(self, data):
        self.asteroids = []
        for y, row in enumerate(data):
            for x, value in enumerate(row):
                if value == '#':
                    self.asteroids.append(Point(x, y))

    def get_most_seen(self):
        asteroid_angles = [self.get_angles(asteroid) for asteroid in self.asteroids]
        unique_counts = [len(asteroid) for asteroid in asteroid_angles]
        max_count = max(unique_counts)
        asteroid_index = unique_counts.index(max_count)
        return self.asteroids[asteroid_index], max_count

    def get_destruction_order(self, location):
        destruction_order = []

        angles = self.get_angles(location)
        odered_angles = [angle for angle in angles]
        odered_angles.sort()

        for angle in odered_angles:
            asteroids = angles[angle]
            distances = [location.distance(asteroid) for asteroid in asteroids]
            asteroid = asteroids[distances.index(min(distances))]
            destruction_order.append(asteroid)

        return destruction_order

    def get_angles(self, start):
        angles = defaultdict(list)
        [angles[start.angle(end)].append(end) for end in self.asteroids if end != start]
        return angles

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.asteroids)


def main():
    grid = get_grid()
    most_seen = grid.get_most_seen()
    # Part 1: 230
    print('Part 1: {}'.format(most_seen[1]))
    destruction_order = grid.get_destruction_order(most_seen[0])
    asteroid = destruction_order[199]
    # Part 2: 1205
    print('Part 2: {}'.format((asteroid.x * 100) + asteroid.y))


def get_grid():
    return Grid(Parser().lines())


if __name__ == '__main__':
    main()
