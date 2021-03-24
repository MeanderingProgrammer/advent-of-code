import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Point:

    def __init__(self, x, y, z=0, w=0):
        self.coords = (x, y, z, w)

    def get_neighbors(self):
        neighbors = [self]
        for dimen in range(len(self.coords)):
            length = len(neighbors)
            for i in range(length):
                neighbor = neighbors[i]
                coords = list(neighbor.coords)
                coords[dimen] -= 1
                neighbors.append(Point(*coords))
                coords[dimen] += 2
                neighbors.append(Point(*coords))
        return neighbors[1:]

    def __eq__(self, other):
        return self.coords == other.coords

    def __hash__(self):
        return hash(self.coords)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.coords)

class Status:

    def __init__(self, active=False):
        self.active = active
        self.active_neighbors = 0

    def increment(self):
        self.active_neighbors += 1

    def update_state(self):
        if self.active:
            if self.active_neighbors not in [2, 3]:
                self.active = False
        else:
            if self.active_neighbors == 3:
                self.active = True
        self.active_neighbors = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '#' if self.active else '.'


class Grid:

    def __init__(self):
        self.grid = {}
        self.step_count = 0

    def add(self, point, status):
        self.grid[point] = status

    def step(self):
        self.update_counts()
        self.update_states()
        self.step_count += 1

    def update_counts(self):
        active_points = [point for point in self.grid if self.grid[point].active]
        for active_point in active_points:
            for neighbor in active_point.get_neighbors():
                if neighbor not in self.grid:
                    self.grid[neighbor] = Status()
                self.grid[neighbor].increment()

    def update_states(self):
        for status in self.grid.values():
            status.update_state()

    def get_active(self):
        is_active = [status.active for status in self.grid.values()]
        return sum(is_active)

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        w_bounds = self.get_dimen_bounds(lambda point: point.coords[3])
        z_bounds = self.get_dimen_bounds(lambda point: point.coords[2])
        y_bounds = self.get_dimen_bounds(lambda point: point.coords[1])
        x_bounds = self.get_dimen_bounds(lambda point: point.coords[0])

        for w in range(w_bounds[0], w_bounds[1]+1):
            xs = []
            ys = []
            zs = []
            for z in range(z_bounds[0], z_bounds[1]+1):
                for y in range(y_bounds[1], y_bounds[0]-1, -1):
                    for x in range(x_bounds[0], x_bounds[1]+1):
                        status = self.grid.get(Point(x, y, z, w), Status())
                        if status.active:
                            xs.append(x)
                            ys.append(y)
                            zs.append(z)
            ax.scatter(xs, ys, zs)
            plt.savefig('steps/{}/{}.png'.format(self.step_count, w))
            ax.clear()


    def __str__(self):
        w_bounds = self.get_dimen_bounds(lambda point: point.coords[3])
        z_bounds = self.get_dimen_bounds(lambda point: point.coords[2])
        y_bounds = self.get_dimen_bounds(lambda point: point.coords[1])
        x_bounds = self.get_dimen_bounds(lambda point: point.coords[0])

        result = ''

        for w in range(w_bounds[0], w_bounds[1]+1):
            for z in range(z_bounds[0], z_bounds[1]+1):
                result += 'z = {}, w = {} \n'.format(z, w)
                for y in range(y_bounds[1], y_bounds[0]-1, -1):
                    row = ''
                    for x in range(x_bounds[0], x_bounds[1]+1):
                        status = self.grid.get(Point(x, y, z, w), Status())
                        row += str(status)
                    result += row + '\n'
                result += '\n'

        return result

    def get_dimen_bounds(self, extractor):
        values = [extractor(point) for point in self.grid]
        return min(values), max(values)


def main():
    # Part 1: 284
    # Part 2: 2,240
    grid = get_grid()
    for i in range(6):
        grid.step()
        grid.plot()
    print('Total active cubes = {}'.format(grid.get_active()))


def get_grid():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().splitlines()

    grid = Grid()
    for y, datum in enumerate(data):
        y = len(data) - y - 1
        for x in range(len(datum)):
            status = datum[x]
            grid.add(Point(x, y), Status(status == '#'))
    return grid


if __name__ == '__main__':
    main()

