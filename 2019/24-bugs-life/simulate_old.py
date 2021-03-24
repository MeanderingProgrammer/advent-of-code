H = 5
W = 5

TOP = 'top'
BOTTOM = 'bottom'
LEFT = 'left'
RIGHT = 'right'

class Grid:

    def __init__(self, data):
        self.recursive_grid = [data]

    def step(self):
        self.recursive_grid = [self.new_grid()] + self.recursive_grid + [self.new_grid()]

        next_recursive_grid = []
        for depth, grid in enumerate(self.recursive_grid):
            next_grid = []
            for r, row in enumerate(grid):
                next_row = []
                for c, value in enumerate(row):
                    count = self.count_adjacent(depth, r, c)
                    if r == 2 and c == 2:
                        next_row.append('?')
                    elif value == '#':
                        next_row.append('#' if count == 1 else '.')
                    else:
                        next_row.append('#' if count in [1, 2] else '.')
                next_grid.append(next_row)
            next_recursive_grid.append(next_grid)
        self.recursive_grid = next_recursive_grid

    def count_adjacent(self, depth, r, c):
        points = [
            (r-1, c, BOTTOM),
            (r+1, c, TOP),
            (r, c-1, RIGHT),
            (r, c+1, LEFT)
        ]
        count = 0
        for r, c, direction in points:
            count += self.get_count(depth, r, c, direction)
        return count

    def get_count(self, depth, r, c, direction):
        if r < 0:
            if depth == 0:
                return 0
            else:
                return self.get_value(depth - 1, 1, 2)
        elif r >= W:
            if depth == 0:
                return 0
            else:
                return self.get_value(depth - 1, 3, 2)
        elif c < 0:
            if depth == 0:
                return 0
            else:
                return self.get_value(depth - 1, 2, 1)
        elif c >= W:
            if depth == 0:
                return 0
            else:
                return self.get_value(depth - 1, 2, 3)
        elif r == 2 and c == 2:
            if depth == len(self.recursive_grid) - 1:
                return 0
            else:
                grid = self.recursive_grid[depth + 1]
                return self.sum_direction(grid, direction)
        else:
            return self.get_value(depth, r, c)

    def get_value(self, depth, r, c):
        value = self.recursive_grid[depth][r][c]
        return 1 if value == '#' else 0

    def diversity(self):
        total = 0
        for i, value in enumerate(self.grid.flatten()):
            if value == '#':
                total += pow(2, i)
        return total

    def count_bugs(self):
        count = 0
        for grid in self.recursive_grid:
            for row in grid:
                for value in row:
                    if value == '#':
                        count += 1
        return count

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        result = ''

        num_grids = len(self.recursive_grid)
        depth = ((num_grids - 1) // 2) * -1
        
        for grid in self.recursive_grid:
            result += 'Depth {}:\n'.format(depth)
            for row in grid:
                result += '{}\n'.format(''.join(row))
            result += '\n'
            depth += 1

        return result

    @staticmethod
    def new_grid():
        return [['.' for c in range(W)] for r in range(H)]

    @staticmethod
    def sum_direction(grid, direction):
        if direction == TOP:
            row = grid[0]
        elif direction == BOTTOM:
            row = grid[H - 1]
        elif direction == LEFT:
            row = [row[0] for row in grid]
        elif direction == RIGHT:
            row = [row[W - 1] for row in grid]
        else:
            raise Exception('Unexpected direction: {}'.format(direction))
        values = [value == '#' for value in row]
        return sum(values)


def main():
    #solve_part_1()
    solve_part_2()


def solve_part_1():
    # Part 1 = 32776479
    seen = set()
    grid = get_grid()
    while grid not in seen:
        seen.add(grid)
        grid = grid.step()
    print('Biodiversity = {}'.format(grid.diversity()))


def solve_part_2():
    # Part 2 = 2017
    grid = get_grid()
    for i in range(200):
        grid.step()
    print('Total bugs = {}'.format(grid.count_bugs()))


def get_grid():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().split('\n')
    return Grid([[value for value in datum] for datum in data])


if __name__ == '__main__':
    main()
