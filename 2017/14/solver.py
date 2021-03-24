import collections
from aoc_parser import Parser
from aoc_board import Grid, Point

TEST = False

SIZE = 256
INPUT = 'flqrgnkx' if TEST else 'ffayrhll'

class Knot:

    def __init__(self, size, lengths):
        self.q = collections.deque(range(size))
        self.lengths = lengths

        self.skip_size = 0
        self.skipped = []

    def run_hash(self):
        for time in range(64):
            self.run_once()

    def run_once(self):
        for length in self.lengths:
            temp = [self.q.popleft() for i in range(length)]
            temp.reverse()

            self.q.extend(temp)
            self.q.rotate(-self.skip_size)

            self.skipped.append(length + self.skip_size)
            self.skip_size += 1

    def rotate_back(self):
        self.q.rotate(sum(self.skipped))

    def score(self):
        self.rotate_back()
        return self.q.popleft() * self.q.popleft()

    def dense_hash(self):
        hashed = []

        self.rotate_back()
        as_list = list(self.q)
        for i in range(len(as_list) // 16):
            start = i * 16
            end = start + 16
            block = as_list[start:end]
            hashed.append(self.hash_block(block))

        return ''.join(hashed)

    def binary_hash(self):
        hashed = self.dense_hash()
        binary_blocks = [self.binary_block(value) for value in hashed]
        return ''.join(binary_blocks)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.q)

    @staticmethod
    def hash_block(values):
        hashed = 0
        for value in values:
            hashed ^= value
        hex_value = hex(hashed)[2:]
        return hex_value if len(hex_value) == 2 else '0' + hex_value

    @staticmethod
    def binary_block(value):
        binary = bin(int(value, 16))
        binary = binary[2:]
        to_add = 4 - len(binary)
        return ''.join(['0'] * to_add) + binary


def main():
    points = get_enabled_points()
    # Part 1 = 8190
    print('Total points enabled = {}'.format(len(points)))
    # Part 2 = 1134
    groups = group_points(points)
    print('Total groups = {}'.format(len(groups)))


def group_points(points):
    groups = set()

    for point in points:
        matching_groups = get_matching_groups(point, groups)

        if len(matching_groups) == 0:
            groups.add(frozenset([point]))
        else:
            joined = set([point])
            for matching_group in matching_groups:
                joined |= matching_group
                groups.remove(matching_group)
            groups.add(frozenset(joined))

    return groups
        

def get_matching_groups(point, groups):
    matching_groups = set()
    possiblities = point.adjacent()
    for group in groups:
        if matches_group(possiblities, group):
            matching_groups.add(group)
    return matching_groups

def matches_group(possiblities, group):
    for point in possiblities:
        if point in group:
            return True
    return False


def get_enabled_points(limit=128):
    points = []
    for y in range(limit):
        knot = Knot(SIZE, get_lengths(y))
        knot.run_hash()
        hashed = knot.binary_hash()
        for x, value in enumerate(hashed[:limit]):
            if value == '1':
                points.append(Point(x, y))
    return points


def get_lengths(row):
    suffix = [17, 31, 73, 47, 23]
    values = INPUT + '-' + str(row)
    lengths = [ord(value) for value in values]
    return lengths + suffix


if __name__ == '__main__':
    main()
