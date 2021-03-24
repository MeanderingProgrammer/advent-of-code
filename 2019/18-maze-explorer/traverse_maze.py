import numpy as np
import time


class KeyPosition:

    def __init__(self, key, position):
        self.key, self.position = key, position

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '[{}: {}]'.format(self.key, self.position)


class KeyPath:

    def __init__(self, key_position, distance, keys_needed):
        self.key_position, self.distance, self.keys_needed = key_position, distance, keys_needed

    def key(self):
        return self.key_position.key

    def position(self):
        return self.key_position.position

    def can_travel(self, keys):
        return self.keys_needed.issubset(keys)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} to {} need {}'.format(self.distance, self.key_position, self.keys_needed)


class Node:

    def __init__(self):
        self.key_paths = []

    def should_go(self, key_path):
        for kp in self.key_paths:
            if kp.key() == key_path.key():
                if kp.distance <= key_path.distance and key_path.keys_needed.issubset(kp.keys_needed):
                    return False
        return True

    def add(self, key_path):
        self.key_paths.append(key_path)

    def get_possible(self, keys):
        possible = set()
        for key_path in self.key_paths:
            if key_path.can_travel(keys):
                possible.add(key_path)
        return possible

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.key_paths)


class Value:

    def __init__(self, value):
        self.value = value

    def is_wall(self):
        return self.value == '#'

    def is_door(self):
        return self.value.isupper()

    def as_key(self):
        return self.value.lower()

    def is_key(self):
        return self.value.islower()

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value


class pojo.Position:

    def __init__(self, x, y):
        self.__x, self.__y = x, y

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def get(self, grid):
        return grid[self.__y][self.__x]

    def adjacent(self):
        return [
            pojo.Position(self.__x + 1, self.__y),
            pojo.Position(self.__x - 1, self.__y),
            pojo.Position(self.__x, self.__y + 1),
            pojo.Position(self.__x, self.__y - 1)
        ]

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {})'.format(self.__x, self.__y)


class maze.Grid:

    def __init__(self, data):
        self.__grid = np.array([[Value(value) for value in datum] for datum in data])
        self.__dimen = self.__grid.shape
        self.__nodes = np.array([[Node() for x in range(self.__dimen[1])] for y in range(self.__dimen[0])])
        self.__key_positions = self.__get_key_positions()

    def solve(self):
        for key_position in self.__key_positions:
            self.__expand_nodes(key_position, key_position.position, set(), 0)
            print('Done Exapanding: {}'.format(key_position))
        return self.__get_distance(self.__get_position(), set(), {})

    def __get_distance(self, position, keys_acquired, cache):
        if len(keys_acquired) == len(self.__key_positions):
            return 0
        
        min_dist = None
        for possible in position.get(self.__nodes).get_possible(keys_acquired):
            key = possible.key_position.key.value
            if key not in keys_acquired:
                next_position = possible.key_position.position
                next_keys = set(keys_acquired) | set([key])
                cache_key = (next_position, tuple(next_keys))
                if cache_key not in cache:
                    distance = self.__get_distance(next_position, next_keys, cache)
                    cache[cache_key] = distance
                else:
                    distance =  cache[cache_key]
                distance += possible.distance

                if min_dist is None or distance < min_dist:
                    min_dist = distance

        return min_dist

    def __get_key_positions(self):
        key_positions = set()
        for y in range(len(self.__grid)):
            for x in range(len(self.__grid[y])):
                position = pojo.Position(x, y)
                value = position.get(self.__grid)
                if value.is_key():
                    key_positions.add(KeyPosition(value, position))
        return key_positions

    def __expand_nodes(self, key_position, position, keys_needed, distance):
        value = position.get(self.__grid)
        if value.is_door():
            keys_needed = set(keys_needed)
            keys_needed |= set([value.as_key()])

        node = position.get(self.__nodes)
        node.add(KeyPath(key_position, distance, keys_needed))

        for adjacent in position.adjacent():
            if self.__can_go(adjacent):
                adjacent_node = adjacent.get(self.__nodes)
                if adjacent_node.should_go(KeyPath(key_position, distance + 1, keys_needed)):
                    self.__expand_nodes(key_position, adjacent, keys_needed, distance + 1)

    def __get_position(self):
        position = np.where(self.__grid == '@')
        return pojo.Position(position[1][0], position[0][0])

    def __can_go(self, position):
        if position.x() < 0 or position.x() >= self.__dimen[1]:
            return False
        if position.y() < 0 or position.y() >= self.__dimen[0]:
            return False
        value = position.get(self.__grid)
        return not value.is_wall()

    def __str__(self):
        return str(self.__grid)


def main():
    grid = get_grid()
    start_time = time.time()
    steps = grid.solve()
    print('Runtime = {}'.format(time.time() - start_time))
    print('Steps to solve = {}'.format(steps))


def get_grid():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().split('\n')
    return maze.Grid(data)


if __name__ == '__main__':
    main()
