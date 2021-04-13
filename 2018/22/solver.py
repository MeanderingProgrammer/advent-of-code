import heapq 

from commons.aoc_board import Grid, Point


class Region:

    def __init__(self, depth, target, location, left, below):
        self.depth = depth
        self.target = target
        self.location = location
        self.left = left
        self.below = below

        self.geo = None
        self.ero = None
        self.typ = None

    def geologic_index(self):
        if self.geo is not None:
            return self.geo

        if self.location in [Point(0, 0), self.target]:
            self.geo = 0
        elif self.location.y() == 0:
            self.geo = self.location.x() * 16_807
        elif self.location.x() == 0:
            self.geo = self.location.y() * 48_271
        else:
            self.geo = self.left.erosion_level() * self.below.erosion_level()

        return self.geo

    def erosion_level(self):
        if self.ero is not None:
            return self.ero

        self.ero = (self.geologic_index() + self.depth) % 20_183
        return self.ero

    def type(self):
        if self.typ is not None:
            return self.typ

        self.typ = self.erosion_level() % 3
        return self.typ

    def __repr__(self):
        return str(self)

    def __str__(self):
        region_type = self.type()
        if region_type == 0:
            return '.'
        elif region_type == 1:
            return '='
        elif region_type == 2:
            return '|'
        else:
            raise Exception('Unknown type {}'.format(region_type))


GEAR = 'g'
TORCH = 't'
NEITHER = 'n'

VALID_TOOL = {
    0: set([GEAR, TORCH]),
    1: set([GEAR, NEITHER]),
    2: set([TORCH, NEITHER])
}


def main():
    target = Point(14, 778)
    cave = build_out_cave(11_541, target)

    risk_levels = []
    for point, value in cave.items():
        if point <= target:
            risk_levels.append(value.type())
    # Part 1: 11575
    print('Part 1: {}'.format(sum(risk_levels)))

    took = traverse(cave, Point(0, 0), target, TORCH)
    # Part 2: 1068
    print('Part 2: {}'.format(took))


def build_out_cave(depth, target):
    buff = 30
    grid = Grid()
    for x in range(target.x() + 1 + buff):
        for y in range(target.y() + 1 + buff):
            location = Point(x, y)
            grid[location] = Region(
                depth,
                target,
                location,
                grid[location.left()],
                grid[location.down()]
            )
    return grid


def traverse(cave, start, end, equipped):
    queue, seen = [], set()
    heapq.heappush(queue, (0, (start, equipped)))

    while len(queue) > 0:
        time, (location, item) = heapq.heappop(queue)
        if (location, item) in seen:
            continue

        seen.add((location, item))

        if location == end and item == TORCH:
            return time
        elif location == end:
            heapq.heappush(queue, (time + 7, (location, TORCH)))
        else:
            valid_items_in_current_location = VALID_TOOL[cave[location].type()]
            for adjacent in [adjacent for adjacent in location.adjacent() if adjacent in cave]:
                valid_items_in_adjacent = VALID_TOOL[cave[adjacent].type()]
                if item in valid_items_in_adjacent:
                    combination = adjacent, item
                    if combination not in seen:
                        heapq.heappush(queue, (time + 1, combination))
                else:
                    valid_items = valid_items_in_adjacent & valid_items_in_current_location
                    for other_item in valid_items:
                        combination = location, other_item
                        if combination not in seen:
                            heapq.heappush(queue, (time + 7, combination))


if __name__ == '__main__':
    main()
