from computer import Computer


DEBUG = False

WALL = 0
EMPTY = 1
OXYGEN_SYSTEM = 2

DIRECTIONS = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}

OPPOSITES = {
    1: 2,
    2: 1,
    3: 4,
    4: 3
}


class RepairDroid:

    def __init__(self, memory):
        self.__computer = Computer(memory, self, DEBUG)
        self.__completed = False

        self.__position = (0, 0)
        self.__next_position = None
        self.__path = [(0, self.__position)]
        self.__grid = {
            self.__position: EMPTY
        }

    def run(self):
        while self.__computer.has_next() and not self.__completed:
            self.__computer.next()

    def get_input(self):
        unexplored = self.__get_unexplored()
        if len(unexplored) > 0:
            self.__next_position = unexplored[0]
            return self.__next_position[0]
        elif len(self.__path) > 1:
            # If there is nowhere new to explore then we should go back
            previous = self.__path[-1]
            self.__next_position = self.__path[-2]
            self.__path = self.__path[:-2]
            return OPPOSITES[previous[0]]
        else:
            self.__completed = True

    def add_output(self, status):
        # Make sure we can identify the status code
        if status not in [WALL, EMPTY, OXYGEN_SYSTEM]:
            raise Exception('Unexpected status code: {}'.format(status))
        next_position = self.__next_position[1]
        # No matter the status we now know something about the new position
        self.__grid[next_position] = status
        # Identify that oxygen system is found so we can break out of loop
        self.__oxygen_found = status == OXYGEN_SYSTEM
        # If we can move to the given position then go
        if status in [EMPTY, OXYGEN_SYSTEM]:
            self.__position = next_position
            self.__path.append(self.__next_position)

    def get_empty_locations(self):
        return [location for location in self.__grid if self.__grid[location] == EMPTY]

    def get_min_steps(self, position):
        path = [position]
        min_path = self.__get_path(position, path)
        return len(min_path) - 1

    def __get_path(self, position, path):
        if self.__grid.get(position, EMPTY) == OXYGEN_SYSTEM:
            return path

        options = self.__get_options(position)
        options = [option for option in options if option not in path]

        min_path = None

        for option in options:
            path_copy = path + [option]
            result = self.__get_path(option, path_copy)
            if result is not None:
                if min_path is None or len(result) < len(min_path):
                    min_path = result

        return min_path

    def __get_unexplored(self):
        unexplored = []
        for code, direction in DIRECTIONS.items():
            next_position = tuple([sum(component) for component in zip(self.__position, direction)])
            if next_position not in self.__grid:
                unexplored.append((code, next_position))
        return unexplored

    def __get_options(self, position):
        options = []
        for code, direction in DIRECTIONS.items():
            next_position = tuple([sum(component) for component in zip(position, direction)])
            outcome = self.__grid.get(next_position, WALL)
            if outcome != WALL:
                options.append(next_position)
        return options

    def __str__(self):
        return str(self.__grid)


def main():
    droid = RepairDroid(get_memory())
    droid.run()
    # Part 1: 224
    print('Part 1: {}'.format(droid.get_min_steps((0, 0))))
    # Part 2: 284
    print('Part 2: {}'.format(time_for_air(droid)))


def time_for_air(droid):
    # Can optimize by storing optimal paths in cache since we
    # know all subpaths lengths
    steps_needed = []
    empty_locations = droid.get_empty_locations()
    for empty_location in empty_locations:
        steps_needed.append(droid.get_min_steps(empty_location))
    return max(steps_needed)


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
