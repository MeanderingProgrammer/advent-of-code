from dataclasses import dataclass

from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser

LEFT = "<"
RIGHT = ">"
UP = "^"
DOWN = "v"

OPPOSITES: dict[str, str] = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}

AS_POSITION: dict[str, Point] = {
    LEFT: Point(-1, 0),
    RIGHT: Point(1, 0),
    UP: Point(0, -1),
    DOWN: Point(0, 1),
}

INTERSECTION_OPTIONS: dict[str, list[str]] = {
    LEFT: [DOWN, LEFT, UP],
    RIGHT: [UP, RIGHT, DOWN],
    UP: [LEFT, UP, RIGHT],
    DOWN: [RIGHT, DOWN, LEFT],
}


@dataclass
class Cart:
    position: Point
    direction: str
    choice: int

    def go(self, options: list[Point]) -> None:
        if len(options) == 4:
            self.handle_intersection()
        elif len(options) == 2:
            self.standard_movement(options)
        else:
            raise Exception("Unhandled number of options")

    def handle_intersection(self) -> None:
        options = INTERSECTION_OPTIONS[self.direction]
        self.direction = options[self.choice % len(options)]
        self.choice += 1
        self.position += AS_POSITION[self.direction]

    def standard_movement(self, options: list[Point]) -> None:
        opposite = OPPOSITES[self.direction]
        dont_go = self.position + AS_POSITION[opposite]
        options.remove(dont_go)
        if len(options) != 1:
            raise Exception("Unable to eliminate enough options")
        new_position = options[0]
        self.direction = self.how_to_get(new_position)
        self.position = new_position

    def how_to_get(self, new_position: Point) -> str:
        for direction in AS_POSITION:
            if self.position + AS_POSITION[direction] == new_position:
                return direction
        raise Exception("Unable to determine how to reach position")


@dataclass(frozen=True)
class CartSystem:
    track: Grid
    carts: list[Cart]
    crash_positions: list[Point]

    def run(self) -> None:
        while len(self.carts) > 1:
            self.tick()

    def tick(self) -> None:
        carts_crashed: list[Cart] = []
        self.carts.sort(key=lambda cart: cart.position)
        for cart in self.carts:
            cart.go(self.get_options(cart.position))
            new_position = cart.position
            at_same_position = self.carts_at(new_position)
            if len(at_same_position) > 1:
                self.crash_positions.append(new_position)
                carts_crashed.extend(at_same_position)
        for cart_crashed in carts_crashed:
            self.carts.remove(cart_crashed)

    def get_options(self, point: Point) -> list[Point]:
        value = self.track[point]
        if value == "+":
            return [point.left(), point.right(), point.up(), point.down()]
        elif value == "|":
            return [point.up(), point.down()]
        elif value == "-":
            return [point.left(), point.right()]
        elif value == "/":
            if self.track[point.up()] in ["|", "+"]:
                return [point.up(), point.right()]
            else:
                return [point.down(), point.left()]
        elif value == "\\":
            if self.track[point.up()] in ["|", "+"]:
                return [point.up(), point.left()]
            else:
                return [point.down(), point.right()]
        else:
            raise Exception("Unknown value at point")

    def carts_at(self, position: Point) -> list[Cart]:
        return [cart for cart in self.carts if cart.position == position]


def main() -> None:
    system = run_system()
    answer.part1(Point(86, 118), system.crash_positions[0])
    answer.part2(Point(2, 81), system.carts[0].position)


def run_system() -> CartSystem:
    data: dict[Point, str] = dict()
    for y, row in enumerate(Parser().nested_lines()):
        for x, value in enumerate(row):
            data[Point(x, y)] = value
    system = CartSystem(
        track=get_track(data), carts=get_carts(data), crash_positions=[]
    )
    system.run()
    return system


def get_track(data: dict[Point, str]) -> Grid:
    track = Grid()
    for point, value in data.items():
        if value != " ":
            value = "-" if value in [LEFT, RIGHT] else value
            value = "|" if value in [UP, DOWN] else value
            track[point] = value
    return track


def get_carts(data: dict[Point, str]) -> list[Cart]:
    carts: list[Cart] = []
    for point, value in data.items():
        if value in AS_POSITION:
            carts.append(Cart(position=point, direction=value, choice=0))
    return carts


if __name__ == "__main__":
    main()
