class Point:

    def __init__(self, x, y, step=0):
        self.x, self.y = x, y
        self.step = step

    def __add__(self, other):
        return Point(
            self.x+other.x,
            self.y+other.y,
            self.step + 1
        )

    def __len__(self):
        return self.step

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y, self.step)

POINT_MAPPING = {
    'R': Point(1, 0),
    'L': Point(-1, 0),
    'U': Point(0, 1),
    'D': Point(0, -1)
}

class Path:

    def __init__(self, path):
        self.parts = path.split(',')

    def intersection(self, other):
        p1 = set(self.points())
        p1_steps = {}
        for point in p1:
            p1_steps[point] = point.step

        p2 = set(other.points())
        p2_steps = {}
        for point in p2:
            p2_steps[point] = point.step

        counts = []
        intersection = p1.intersection(p2)
        intersection.remove(Point(0, 0))
        for intersectio in intersection:
            counts.append(p1_steps[intersectio] + p2_steps[intersectio])

        return min(counts)

    def points(self):
        points = [Point(0, 0)]
        for part in self.parts:
            direction = POINT_MAPPING[part[0]]
            amount = int(part[1:])
            for i in range(amount):
                new_point = points[-1] + direction
                points.append(new_point)
        return points

def main():
    p1, p2 = get_paths()
    lowest = p1.intersection(p2)
    print('Closest intersection = {}'.format(lowest))


def get_paths():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read()
    data = data.split('\n')
    return Path(data[0]), Path(data[1])


if __name__ == '__main__':
    main()
