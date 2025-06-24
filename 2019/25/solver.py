import itertools
from collections.abc import Generator
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser

BAD_ITEMS = [
    "giant electromagnet",
    "molten lava",
    "photons",
    "escape pod",
    "infinite loop",
]


class Direction(StrEnum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


OPPOSITES: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}


@dataclass(frozen=True)
class View:
    name: str
    directions: list[Direction]
    items: list[str]


@dataclass
class Game:
    instruction: str = ""
    view: View | None = None

    def add(self, ch: str) -> None:
        self.instruction += ch

    def location(self):
        return self.get_view().name

    def is_checkpoint(self) -> bool:
        return self.location() == "Security Checkpoint"

    def directions(self) -> list[Direction]:
        directions = self.get_view().directions
        # Remove direction which takes us to analyzer, for initial traversal
        return directions[1:] if self.is_checkpoint() else directions

    def items(self) -> list[str]:
        return [item for item in self.get_view().items if item not in BAD_ITEMS]

    def get_view(self) -> View:
        if self.view is not None:
            return self.view
        name, directions, items = "", [], []
        for group in self.instruction.split("\n\n"):
            values = [value for value in group.split("\n") if value != ""]
            if len(values) == 0:
                continue
            if values[0].startswith("=="):
                name = values[0][3:-3]
            elif values[0] == "Doors here lead:":
                directions = [Direction(value[2:]) for value in values[1:]]
            elif values[0] == "Items here:":
                items = [value[2:] for value in values[1:]]
        view = View(name=name, directions=directions, items=items)
        self.view = view
        return view

    def get_key(self) -> int:
        lines = [line for line in self.instruction.split("\n") if len(line) > 0]
        return int(lines[-1].split()[-8])


@dataclass(frozen=True)
class Graph:
    graph: dict[str, set[tuple[Direction, str]]]

    def add_node(self, name: str) -> None:
        if name not in self.graph:
            self.graph[name] = set()

    def add_edge(self, start: str, direction: Direction, end: str) -> None:
        self.graph[start].add((direction, end))
        self.graph[end].add((OPPOSITES[direction], start))

    def get_unexplored(self, name: str, directions: list[Direction]) -> list[Direction]:
        explored: list[Direction] = [edge[0] for edge in self.graph[name]]
        return [direction for direction in directions if direction not in explored]


class State(StrEnum):
    EXPLORING = auto()
    SOLVING = auto()


@dataclass(frozen=True)
class ItemBag:
    items: list[str]

    def add(self, item: str) -> None:
        self.items.append(item)

    def next(self):
        for length in range(1, len(self.items) + 1):
            for subset in itertools.combinations(self.items, length):
                yield subset


class DroidBus(Bus):
    def __init__(self):
        # Storing output of game and move to make
        self.game: Game = Game()
        self.commands: list[str] = []
        self.state: State = State.EXPLORING

        # State information to be able to traverse ship
        self.grid: Graph = Graph(graph=dict())
        self.previous: tuple[str, Direction] | None = None
        self.history: list[Direction] = []
        self.path_to_checkpoint: list[Direction] = []

        # For solving final puzzle where all items are needed
        self.items: ItemBag = ItemBag(items=[])
        self.item_generator: Generator[tuple[str, ...], None, None] = self.items.next()

    @override
    def active(self) -> bool:
        return True

    @override
    def add_output(self, value: int) -> None:
        self.game.add(chr(value))

    @override
    def get_input(self) -> int:
        if len(self.commands) == 0:
            if self.state == State.EXPLORING:
                if not self.continue_exploring():
                    [self.add_command(command) for command in self.path_to_checkpoint]
                    self.add_command(Direction.SOUTH)
                    self.state = State.SOLVING
            elif self.state == State.SOLVING:
                self.attempt_solve(True)
            else:
                raise Exception(f"Unknown state {self.state}")
        return ord(self.commands.pop(0))

    def continue_exploring(self) -> bool:
        for item in self.game.items():
            self.items.add(item)
            self.add_command(f"take {item}")

        if self.game.is_checkpoint():
            self.path_to_checkpoint = list(self.history)

        location = self.game.location()
        self.grid.add_node(location)
        if self.previous is not None:
            self.grid.add_edge(self.previous[0], self.previous[1], location)

        unexplored = self.grid.get_unexplored(location, self.game.directions())

        self.game = Game()
        command = None
        if len(unexplored) > 0:
            command = unexplored[0]
            self.history.append(command)
        elif len(self.history) > 0:
            command = OPPOSITES[self.history[-1]]
            self.history = self.history[:-1]
        else:
            return False
        self.previous = (location, command)
        self.add_command(command)
        return True

    def attempt_solve(self, use_known: bool) -> None:
        self.game = Game()
        for to_drop in self.items.items:
            self.add_command(f"drop {to_drop}")
        # Rather than using the item generate pass the known list of items
        known_solution = ["fixed point", "whirled peas", "antenna", "prime number"]
        items = known_solution if use_known else next(self.item_generator)
        for to_pickup in items:
            self.add_command(f"take {to_pickup}")
        self.add_command(Direction.SOUTH)

    def add_command(self, command: str) -> None:
        program = [ch for ch in command]
        program.append("\n")
        self.commands.extend(program)


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    droid = DroidBus()
    computer = Computer(bus=droid, memory=memory)
    computer.run()
    answer.part1(2622472, droid.game.get_key())


if __name__ == "__main__":
    main()
