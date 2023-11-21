import heapq 
import numpy as np


WALL = '#'
PATH = '.'
MAZE_COMPONENTS = [WALL, PATH]

LEFT = -1
RIGHT = 2


class Path:

    def __init__(self, node, length, level=0):
        self.__node, self.__length, self.__level = node, length, level

    def key(self, ignore_level):
        # Need to use point, as label matches 2 possible values
        if ignore_level:
            return self.__node.point()
        else:
            return self.__node.point(), self.level()

    def label(self):
        return self.__node.label()

    def inner(self):
        return self.__node.inner()

    def level(self):
        return self.__level

    def node(self):
        return self.__node

    def length(self):
        return self.__length

    def __lt__(self, o):
        if self.level() != o.level():
            return self.level() < o.level()
        return self.length() < o.length()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Path to {} = {} at level {}'.format(self.__node, self.__length, self.__level)


class Point:

    def __init__(self, x, y):
        self.__x, self.__y = x, y

    def transpose(self):
        temp = self.__x
        self.__x = self.__y
        self.__y = temp

    def adjacent(self):
        return [
            Point(self.__x-1, self.__y),
            Point(self.__x+1, self.__y),
            Point(self.__x, self.__y-1),
            Point(self.__x, self.__y+1)
        ]

    def get(self, grid):
        return grid[self.__y][self.__x]

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.__x, self.__y)


class Node:

    def __init__(self, values, point, inner):
        self.__is_valid = all([value.isupper() for value in values])
        self.__label = ''.join(values)
        self.__point, self.__inner = point, inner

    def valid(self):
        return self.__is_valid

    def label(self):
        return self.__label

    def point(self):
        return self.__point

    def inner(self):
        return self.__inner

    def transpose(self):
        self.__point.transpose()

    def __repr__(self):
        return str(self)

    def __str__(self):
        style = 'inner' if self.__inner else 'outer'
        return '{} node {} at {}'.format(style, self.__label, self.__point)


class Maze:

    def __init__(self, grid):
        self.__grid = np.array(grid)
        self.__h, self.__w = self.__grid.shape
        self.__inner_size = self.__get_inner_size()

        self.__nodes = self.__get_nodes()
        self.__transpose()
        transposed_nodes = self.__get_nodes()
        [node.transpose() for node in transposed_nodes]
        self.__nodes.extend(transposed_nodes)
        self.__transpose()

        # Here we will have all values as every node has a unique point
        self.__point_to_node = {node.point(): node for node in self.__nodes}
        # This will overwrite values as aside from the start and end 2 nodes
        # will share the same label
        self.__label_to_nodes = {}
        for node in self.__nodes:
            self.__label_to_nodes[(node.label(), node.inner())] = node
        
        self.__graph = self.__get_graph()

    def get_path(self, start, end, ignore_level):
        start = self.__label_to_nodes[start, False]
        return self.__path_between(start, end, ignore_level)

    def __path_between(self, start, end, ignore_level):
        seen = set()

        queue = []
        heapq.heappush(queue, Path(start, 0))

        while len(queue) > 0:
            path = heapq.heappop(queue)
            if path.label() == end:
                return path.length()

            if path.key(ignore_level) not in seen:
                seen.add(path.key(ignore_level))
                neighbors = self.__get_neighbors(path)

                for neighbor in neighbors:
                    if ignore_level:
                        heapq.heappush(queue, neighbor)
                    else:
                        if neighbor.label() in ['AA', 'ZZ']:
                            if neighbor.level() == 0:
                                heapq.heappush(queue, neighbor)
                        else:
                            if neighbor.level() >= 0:
                                heapq.heappush(queue, neighbor)

    def __get_neighbors(self, path):
        neighbors = []
        for neighbor in self.__graph[path.node()]:
            if neighbor.label() in ['AA', 'ZZ']:
                neighbors.append(Path(
                    neighbor.node(),
                    path.length() + neighbor.length(),
                    path.level()
                ))
            else:
                output_neighbor = self.__label_to_nodes[(neighbor.label(), not neighbor.inner())]
                neighbors.append(Path(
                    output_neighbor,
                    path.length() + neighbor.length() + 1,
                    path.level() + (1 if neighbor.inner() else -1)
                ))
        return neighbors

    def __get_inner_size(self):
        # Get middle row, check number of elements that are maze what we consider
        # components of a maze, divide by 2 assuming uniform inner size
        middle_row = self.__grid[self.__h // 2][2:-2]
        part_of_maze = [value in MAZE_COMPONENTS for value in middle_row]
        return sum(part_of_maze) // 2

    def __get_nodes(self):
        starting_points = [
            (0, RIGHT, False), 
            (2 + self.__inner_size, LEFT, True), 
            (self.__w - self.__inner_size -2 - 2, RIGHT, True), 
            (self.__w - 2, LEFT, False)
        ]

        nodes = []

        for r, row in enumerate(self.__grid):
            for starting_point, offset, inner in starting_points:
                node = Node(
                    row[starting_point:starting_point+2],
                    Point(starting_point + offset, r),
                    inner
                )
                print(node.valid())
                if node.valid():
                    nodes.append(node)

        return nodes

    def __transpose(self):
        self.__grid = np.transpose(self.__grid)
        self.__h, self.__w = self.__grid.shape

    def __get_graph(self):
        graph = {}
        for node in self.__nodes:
            graph[node] = self.__explore_point(node.point(), set(), 0)[1:]
        return graph

    def __explore_point(self, point, explored, length):
        explored.add(point)

        paths = []
        if point in self.__point_to_node:
            node = self.__point_to_node[point]
            paths.append(Path(node, length))

        for adjacent in point.adjacent():
            value = adjacent.get(self.__grid)
            if value == PATH and adjacent not in explored:
                paths.extend(self.__explore_point(adjacent, explored, length + 1))
        return paths

    def __str__(self):
        return str(self.__grid)


def main():
    maze = get_maze()
    # Part 1: 628
    #print('Part 1: {}'.format(maze.get_path('AA', 'ZZ', True)))
    # Part 2: 7506
    #print('Part 2: {}'.format(maze.get_path('AA', 'ZZ', False)))


def get_maze():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read()
    data = data.split('\n')
    data = [[value for value in datum] for datum in data]
    return Maze(data)


if __name__ == '__main__':
    main()
