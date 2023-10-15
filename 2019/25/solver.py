import itertools
from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser
from dataclasses import dataclass
from typing import List

BAD_ITEMS = [
    "giant electromagnet",
    "molten lava",
    "photons",
    "escape pod",
    "infinite loop",
]

SECURITY = "Security Checkpoint"


@dataclass(frozen=True)
class Direction:
    value: str

    def opposite(self) -> "Direction":
        OPPOSITES = {"north": "south", "south": "north", "east": "west", "west": "east"}
        return Direction(OPPOSITES[self.value])

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value


class Game:
    def __init__(self):
        self.instruction = ""

    def add(self, ch):
        self.instruction += ch

    def clear(self):
        self.instruction = ""

    def location(self):
        components = self.get_componenets()
        likely_location = components[0][0]
        return likely_location[3:-3]

    def directions(self) -> List[Direction]:
        components = self.get_componenets()
        likely_directions = components[1][1:]
        # Remove direction which takes us to analyzer, for initial traversal
        if self.is_checkpoint():
            likely_directions = likely_directions[1:]
        return [
            Direction(likely_direction[2:]) for likely_direction in likely_directions
        ]

    def items(self):
        components = self.get_componenets()
        if len(components) == 3:
            likely_items = [likely_item[2:] for likely_item in components[2][1:]]
            return [item for item in likely_items if item not in BAD_ITEMS]
        else:
            return []

    def is_checkpoint(self):
        return self.location() == SECURITY

    def get_componenets(self):
        components = [
            [component for component in components.split("\n") if component != ""]
            for components in self.instruction.split("\n\n")
        ]
        last_index = len(components) - components[::-1].index([]) - 1
        return components[last_index + 1 : -1]

    def get_key(self):
        key_line = self.instruction.split("\n")[-2]
        key_parts = key_line.split()
        return int(key_parts[-8])

    def __str__(self):
        return self.instruction


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, name):
        if name not in self.graph:
            self.graph[name] = set()

    def add_edge(self, start, direction, end):
        self.graph[start].add((direction, end))
        self.graph[end].add((direction.opposite(), start))

    def get_unexplored(self, name, directions):
        explored = [edge[0] for edge in self.graph[name]]
        return [direction for direction in directions if direction not in explored]

    def __str__(self):
        values = ["{}: {}".format(name, self.graph[name]) for name in self.graph]
        return "\n".join(values)


class ItemBag:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def next(self):
        for l in range(1, len(self.items) + 1):
            for subset in itertools.combinations(self.items, l):
                yield subset

    def __str__(self):
        return str(self.items)


class DroidBus:
    def __init__(self):
        # Storing output of game and move to make
        self.game = Game()
        self.move = []

        # State information to be able to traverse ship
        self.grid = Graph()
        self.previous = None
        self.history = []
        self.exploring = True

        # For solving final puzzle where all items are needed
        self.solving = False
        self.path_to_security = None
        self.items = ItemBag()
        self.item_generator = self.items.next()

    def get_input(self):
        if len(self.move) == 0:
            if self.exploring:
                self.exploring &= self.continue_exploring()

            if self.solving:
                self.attempt_solve(True)

            if not self.exploring and not self.solving:
                for move in self.path_to_security:
                    self.move.extend(self.__transform(str(move)))
                self.move.extend(self.__transform(str("south")))
                self.solving = True

        return ord(self.move.pop(0))

    def add_output(self, value: int) -> None:
        self.game.add(chr(value))

    def continue_exploring(self):
        for item in self.game.items():
            self.items.add(item)
            self.move.extend(self.__transform("take {}".format(item)))

        location = self.game.location()
        directions = self.game.directions()
        if self.game.is_checkpoint():
            self.path_to_security = [direction for direction in self.history]

        self.grid.add_node(location)
        if self.previous is not None:
            self.grid.add_edge(self.previous[0], self.previous[1], location)

        unexplored = self.grid.get_unexplored(location, directions)

        # Done exploring the ship, all paths explored, nothing to recurse back to
        if len(unexplored) == 0 and len(self.history) == 0:
            return False

        self.game.clear()

        if len(unexplored) > 0:
            move = unexplored[0]
            self.history.append(move)
        else:
            move = self.history[-1].opposite()
            self.history = self.history[:-1]

        self.previous = (location, move)
        self.move.extend(self.__transform(str(move)))
        return True

    def attempt_solve(self, use_known: bool):
        self.game.clear()
        for to_drop in self.items.items:
            self.move.extend(self.__transform("drop {}".format(to_drop)))
        # Rather than using the item generate pass the known list of items
        known_solution = ["fixed point", "whirled peas", "antenna", "prime number"]
        items = known_solution if use_known else next(self.item_generator)
        for to_pickup in items:
            self.move.extend(self.__transform("take {}".format(to_pickup)))
        self.move.extend(self.__transform("south"))

    @staticmethod
    def __transform(move):
        program = [ch for ch in move]
        program.append("\n")
        return program


def main():
    memory, droid = Parser().int_csv(), DroidBus()
    computer = Computer(droid)
    computer.set_memory(memory)
    computer.run()
    answer.part1(2622472, droid.game.get_key())


if __name__ == "__main__":
    main()
