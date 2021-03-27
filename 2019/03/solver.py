class Point:

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Point(
            self.x+other.x,
            self.y+other.y,
        )

    def __len__(self):
        return abs(self.x) + abs(self.y)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)


POINT_MAPPING = {
    'R': Point(1, 0),
    'L': Point(-1, 0),
    'U': Point(0, 1),
    'D': Point(0, -1)
}


class Path:

    def __init__(self, path):
        self.points, self.step_counts = self.all_points_on_path(path.split(','))

    def get_intersection(self, other):
        return self.points & other.points

    def steps(self, location):
        return self.step_counts[location]

    @staticmethod
    def all_points_on_path(parts):
        points, step_counts, steps = [Point(0, 0)], {}, 0
        for part in parts:
            direction = POINT_MAPPING[part[0]]
            for i in range(int(part[1:])):
                steps += 1
                new_point = points[-1] + direction
                points.append(new_point)
                if new_point not in step_counts:
                    step_counts[new_point] = steps
        return set(points[1:]), step_counts


def main():
    p1, p2 = get_paths()
    intersections = p1.get_intersection(p2)
    lengths = [len(intersection) for intersection in intersections]
    # Part 1: 870
    print('Part 1: {}'.format(min(lengths)))
    steps = [p1.steps(intersection) + p2.steps(intersection) for intersection in intersections]
    # Part 2: 13698
    print('Part 2: {}'.format(min(steps)))


def get_paths():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read()
    data = data.split('\n')
    return Path(data[0]), Path(data[1])


if __name__ == '__main__':
    main()
