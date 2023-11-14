import math
from dataclasses import dataclass
from typing import Callable, Self

from aoc import answer
from aoc.parser import Parser

Vector = tuple[int, int, int]


def add(v1: Vector, v2: Vector) -> Vector:
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])


def negative(v: Vector) -> Vector:
    return (-v[0], -v[1], -v[2])


def energy(v: Vector) -> int:
    return abs(v[0]) + abs(v[1]) + abs(v[2])


def simple(value: int) -> int:
    if value < 0:
        return 1
    elif value > 0:
        return -1
    else:
        return 0


@dataclass
class Body:
    position: Vector
    velocity: Vector

    def add_gravity(self, other: Self) -> None:
        difference = add(self.position, negative(other.position))
        gx, gy, gz = [simple(value) for value in difference]
        self.velocity = add(self.velocity, (gx, gy, gz))

    def apply_velocity(self) -> None:
        self.position = add(self.position, self.velocity)

    def energy(self) -> int:
        return energy(self.position) * energy(self.velocity)

    def extract(self, extractor: Callable[[Vector], int]) -> tuple[int, int]:
        return extractor(self.position), extractor(self.velocity)


@dataclass(frozen=True)
class System:
    bodies: list[Body]

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


def main() -> None:
    answer.part1(5350, run_for(1_000))
    answer.part2(467034091553512, get_system_period())


def run_for(n: int) -> int:
    system = get_system()
    for _ in range(n):
        system.step()
    return system.energy()


def get_system_period() -> int:
    def lcm(a: int, b: int) -> int:
        return abs(a * b) // math.gcd(a, b)

    x_period, y_period, z_period = component_periods()
    return lcm(lcm(x_period, y_period), z_period)


def component_periods() -> tuple[int, int, int]:
    system = get_system()
    x_goal = system.extract(lambda v: v[0])
    y_goal = system.extract(lambda v: v[1])
    z_goal = system.extract(lambda v: v[2])

    x_period, y_period, z_period = None, None, None
    system, step = get_system(), 0
    while x_period is None or y_period is None or z_period is None:
        system.step()
        step += 1
        if x_period is None and x_goal == system.extract(lambda v: v[0]):
            x_period = step
        if y_period is None and y_goal == system.extract(lambda v: v[1]):
            y_period = step
        if z_period is None and z_goal == system.extract(lambda v: v[2]):
            z_period = step
    return x_period, y_period, z_period


def get_system() -> System:
    def parse_vector(line: str) -> Vector:
        x, y, z = [int(part.split("=")[1]) for part in line[1:-1].split(", ")]
        return x, y, z

    return System(
        bodies=[
            Body(position=parse_vector(line), velocity=(0, 0, 0))
            for line in Parser().lines()
        ]
    )


if __name__ == "__main__":
    main()
