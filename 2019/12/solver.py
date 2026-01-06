import math
from dataclasses import dataclass
from typing import Callable, Self

from aoc import answer
from aoc.parser import Parser

type Vector = tuple[int, int, int]


def add(v1: Vector, v2: Vector) -> Vector:
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])


def substract(v1: Vector, v2: Vector) -> Vector:
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])


def clamp(v: Vector) -> Vector:
    return (simple(v[0]), simple(v[1]), simple(v[2]))


def simple(value: int) -> int:
    if value < 0:
        return -1
    elif value > 0:
        return 1
    else:
        return 0


def energy(v: Vector) -> int:
    return abs(v[0]) + abs(v[1]) + abs(v[2])


@dataclass(frozen=True)
class System:
    bodies: list[Body]

    @classmethod
    def new(cls, lines: list[str]) -> Self:
        return cls(bodies=[Body.new(line) for line in lines])

    def step(self) -> None:
        for body in self.bodies:
            others = [other for other in self.bodies if other != body]
            for other in others:
                body.add_gravity(other)
        [body.apply_velocity() for body in self.bodies]

    def energy(self) -> int:
        return sum([body.energy() for body in self.bodies])

    def extract(self, extractor: Callable[[Vector], int]) -> list[tuple[int, int]]:
        return [body.extract(extractor) for body in self.bodies]


@dataclass
class Body:
    position: Vector
    velocity: Vector

    @classmethod
    def new(cls, s: str) -> Self:
        x, y, z = [int(part.split("=")[1]) for part in s[1:-1].split(", ")]
        return cls((x, y, z), (0, 0, 0))

    def add_gravity(self, other: Self) -> None:
        difference = substract(self.position, other.position)
        self.velocity = substract(self.velocity, clamp(difference))

    def apply_velocity(self) -> None:
        self.position = add(self.position, self.velocity)

    def energy(self) -> int:
        return energy(self.position) * energy(self.velocity)

    def extract(self, extractor: Callable[[Vector], int]) -> tuple[int, int]:
        return extractor(self.position), extractor(self.velocity)


@answer.timer
def main() -> None:
    lines = Parser().lines()
    answer.part1(5350, run(lines, 1_000))
    answer.part2(467034091553512, system_period(lines))


def run(lines: list[str], n: int) -> int:
    system = System.new(lines)
    for _ in range(n):
        system.step()
    return system.energy()


def system_period(lines: list[str]) -> int:
    def lcm(a: int, b: int) -> int:
        return abs(a * b) // math.gcd(a, b)

    system = System.new(lines)
    period = component_periods(system)
    return lcm(lcm(period[0], period[1]), period[2])


def component_periods(system: System) -> Vector:
    x_goal = system.extract(lambda v: v[0])
    y_goal = system.extract(lambda v: v[1])
    z_goal = system.extract(lambda v: v[2])

    step = 0
    period: Vector = 0, 0, 0
    while period[0] == 0 or period[1] == 0 or period[2] == 0:
        system.step()
        step += 1
        if period[0] == 0 and x_goal == system.extract(lambda v: v[0]):
            period = step, period[1], period[2]
        if period[1] == 0 and y_goal == system.extract(lambda v: v[1]):
            period = period[0], step, period[2]
        if period[2] == 0 and z_goal == system.extract(lambda v: v[2]):
            period = period[0], period[1], step
    return period


if __name__ == "__main__":
    main()
