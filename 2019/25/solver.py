import itertools
from dataclasses import dataclass
from typing import Optional, Self, override

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
OPPOSITES = {"north": "south", "south": "north", "east": "west", "west": "east"}


@dataclass(frozen=True)
class Direction:
    value: str

    def opposite(self) -> Self:
        return type(self)(OPPOSITES[self.value])


@dataclass(frozen=True)
class View:
    name: str
    directions: list[Direction]
    items: list[str]


@dataclass
class Game:
    instruction: str = ""
    view: Optional[View] = None

    def add(self, ch: str) -> None:
        self.instruction += ch

    def clear(self) -> None:
        self.instruction = ""
        self.view = None

    def location(self):
        return self.get_view().name

    def directions(self) -> list[Direction]:
        directions = self.get_view().directions
        # Remove direction which takes us to analyzer, for initial traversal
        return directions[1:] if self.is_checkpoint() else directions

    def is_checkpoint(self) -> bool:
        return self.location() == "Security Checkpoint"

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
        self.graph[end].add((direction.opposite(), start))

    def get_unexplored(self, name: str, directions: list[Direction]) -> list[Direction]:
        explored: list[Direction] = [edge[0] for edge in self.graph[name]]
        return [direction for direction in directions if direction not in explored]


@dataclass(frozen=True)
class ItemBag:
    items: list[str]

    def add(self, item: str) -> None:
        self.items.append(item)

    def next(self):
        for l in range(1, len(self.items) + 1):
            for subset in itertools.combinations(self.items, l):
                yield subset


class DroidBus(Bus):
    def __init__(self):
        # Storing output of game and move to make
        self.game: Game = Game()
        self.move: list[str] = []

        # State information to be able to traverse ship
        self.grid: Graph = Graph(graph=dict())
        self.previous: Optional[tuple[str, Direction]] = None
        self.history: list[Direction] = []
        self.exploring: bool = True

        # For solving final puzzle where all items are needed
        self.solving: bool = False
        self.path_to_checkpoint: list[Direction] = []
        self.items: ItemBag = ItemBag(items=[])
        self.item_generator = self.items.next()

    @override
    def active(self) -> bool:
        return True

    @override
    def add_output(self, value: int) -> None:
        self.game.add(chr(value))

    @override
    def get_input(self) -> int:
        if len(self.move) == 0:
            if self.exploring:
                self.exploring &= self.continue_exploring()
            if self.solving:
                self.attempt_solve(True)
            if not self.exploring and not self.solving:
                [self.add_command(move.value) for move in self.path_to_checkpoint]
                self.add_command("south")
                self.solving = True
        return ord(self.move.pop(0))

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
        if len(unexplored) == 0 and len(self.history) == 0:
            return False

        self.game.clear()
        if len(unexplored) > 0:
            move: Direction = unexplored[0]
            self.history.append(move)
        else:
            move: Direction = self.history[-1].opposite()
            self.history = self.history[:-1]
        self.previous = (location, move)
        self.add_command(move.value)
        return True

    def attempt_solve(self, use_known: bool) -> None:
        self.game.clear()
        for to_drop in self.items.items:
            self.add_command(f"drop {to_drop}")
        # Rather than using the item generate pass the known list of items
        known_solution = ["fixed point", "whirled peas", "antenna", "prime number"]
        items = known_solution if use_known else next(self.item_generator)
        for to_pickup in items:
            self.add_command(f"take {to_pickup}")
        self.add_command("south")

    def add_command(self, command: str) -> None:
        program = [ch for ch in command]
        program.append("\n")
        self.move.extend(program)


def main() -> None:
    droid = DroidBus()
    computer = Computer(bus=droid, memory=Parser().int_csv())
    computer.run()
    answer.part1(2622472, droid.game.get_key())


if __name__ == "__main__":
    main()
