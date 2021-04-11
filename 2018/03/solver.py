import re

from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


CLAIM_PATTERN = '^#(.*) @ (.*),(.*): (.*)x(.*)$'


class Claim:

    def __init__(self, value):
        match = re.match(CLAIM_PATTERN, value)
        self.claim_id = int(match[1])
        self.point = Point(int(match[2]), int(match[3]))
        self.width = int(match[4])
        self.height = int(match[5])

    def get_points(self):
        points = set()
        for x in range(self.width):
            for y in range(self.height):
                points.add(self.point + Point(x, y))
        return points

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} @ {}: {}x{}'.format(
            self.claim_id, self.point, self.width, self.height
        )


def main():
    grid = Grid()
    all_claims = set()

    for line in Parser().lines():
        claim = Claim(line)
        for point in claim.get_points():
            all_claims.add(claim.claim_id)
            if point not in grid:
                grid[point] = []
            grid[point].append(claim.claim_id)

    multiple_claims = 0
    for point, claims_on_point in grid.items():
        if len(claims_on_point) > 1:
            multiple_claims += 1
            for claim_on_point in claims_on_point:
                all_claims.discard(claim_on_point)

    # Part 1: 120408
    print('Part 1: {}'.format(multiple_claims))
    # Part 2: 1276
    print('Part 2: {}'.format(next(iter(all_claims))))


if __name__ == '__main__':
    main()
