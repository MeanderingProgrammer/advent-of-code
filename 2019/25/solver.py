import itertools
from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Self

from aoc import answer
from aoc.intcode import Computer
from aoc.parser import Parser
from aoc.point import Direction

BAD_ITEMS: list[str] = [
    "giant electromagnet",
    "molten lava",
    "photons",
    "escape pod",
    "infinite loop",
]


@dataclass
class View:
    name: str
    directions: list[Direction]
    items: list[str]

    @classmethod
    def new(cls, s: str) -> Self:
        result = cls(name="", directions=[], items=[])
        for group in s.split("\n\n"):
            lines = [value for value in group.split("\n") if value != ""]
            if len(lines) == 0:
                continue
            label = lines.pop(0)
            if label.startswith("=="):
                result.name = label[3:-3]
            elif label == "Doors here lead:":
                result.directions = [Direction.new(line[2:]) for line in lines]
            elif label == "Items here:":
                result.items = [line[2:] for line in lines]
        return result


class State(StrEnum):
    EXPLORING = auto()
    SOLVING = auto()


@dataclass
class Bag:
    items: list[str]
    index: int = 0
    combinations: list[tuple[int, ...]] | None = None

    def add(self, item: str) -> None:
        self.items.append(item)

    def inventory(self) -> list[int]:
        if self.index == 0:
            return list(range(len(self.items)))
        else:
            return self.nth(self.index - 1)

    def next(self) -> list[int]:
        self.index += 1
        return self.nth(self.index - 1)

    def nth(self, i: int) -> list[int]:
        if self.combinations is not None:
            return list(self.combinations[i])

        self.combinations = []
        indices = list(range(len(self.items)))
        for size in range(1, len(indices) + 1):
            for subset in itertools.combinations(indices, size):
                self.combinations.append(subset)
        return self.nth(i)


@dataclass
class DroidBus:
    instruction: str
    commands: list[str]
    state: State
    grid: dict[str, set[Direction]]
    previous: tuple[str, Direction] | None
    history: list[Direction]
    path: list[Direction]
    bag: Bag

    @classmethod
    def new(cls) -> Self:
        bag = Bag(items=[])
        return cls(
            # output of game and move to make
            instruction="",
            commands=[],
            state=State.EXPLORING,
            # state information to be able to traverse ship
            grid=defaultdict(set),
            previous=None,
            history=[],
            path=[],
            # for solving final puzzle where all items are needed
            bag=bag,
        )

    def active(self) -> bool:
        return True

    def add_output(self, value: int) -> None:
        self.instruction += chr(value)

    def get_input(self) -> int:
        if len(self.commands) > 0:
            return ord(self.commands.pop(0))
        match self.state:
            case State.EXPLORING:
                if self.explored():
                    for direction in self.path:
                        self.add_direction(direction)
                    self.add_direction(Direction.DOWN)
                    self.state = State.SOLVING
            case State.SOLVING:
                self.next_solution()
        return self.get_input()

    def explored(self) -> bool:
        view = View.new(self.instruction)
        self.instruction = ""

        location = view.name
        explored = self.grid[location]
        if self.previous is not None:
            self.grid[self.previous[0]].add(self.previous[1])
            explored.add(self.previous[1].opposite())

        for item in view.items:
            if item not in BAD_ITEMS:
                self.bag.add(item)
                self.add_command(f"take {item}")

        directions = view.directions
        if view.name == "Security Checkpoint":
            self.path = self.history.copy()
            # remove direction which takes us to analyzer for initial traversal
            directions.pop()

        direction = None
        unexplored = set(directions).difference(explored)
        if len(unexplored) > 0:
            direction = unexplored.pop()
            self.history.append(direction)
            self.add_direction(direction)
            self.previous = (location, direction)
            return False
        elif len(self.history) > 0:
            direction = self.history.pop().opposite()
            self.add_direction(direction)
            self.previous = (location, direction)
            return False
        else:
            return True

    def next_solution(self) -> None:
        # clear instruction string after each attempt
        self.instruction = ""
        for i in self.bag.inventory():
            self.add_command(f"drop {self.bag.items[i]}")
        for i in self.bag.next():
            self.add_command(f"take {self.bag.items[i]}")
        self.add_direction(Direction.DOWN)

    def get_key(self) -> int:
        lines = self.instruction.split("\n")
        last = [line for line in lines if line != ""][-1]
        return int(last.split()[-8])

    def add_direction(self, direction: Direction) -> None:
        match direction:
            case Direction.UP:
                self.add_command("north")
            case Direction.DOWN:
                self.add_command("south")
            case Direction.LEFT:
                self.add_command("west")
            case Direction.RIGHT:
                self.add_command("east")

    def add_command(self, command: str) -> None:
        program = [ch for ch in command]
        program.append("\n")
        self.commands.extend(program)


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    droid = DroidBus.new()
    computer = Computer(bus=droid, memory=memory)
    computer.run()
    answer.part1(2622472, droid.get_key())


if __name__ == "__main__":
    main()
