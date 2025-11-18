from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser

Vector = tuple[int, int, int]


def parse_vector(value: str) -> tuple[str, Vector]:
    name, value = value.split("=")
    x, y, z = [int(val) for val in value[1:-1].split(",")]
    return name, (x, y, z)


def add(v1: Vector, v2: Vector) -> Vector:
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])


def size(v: Vector) -> int:
    return abs(v[0]) + abs(v[1]) + abs(v[2])


@dataclass
class Particle:
    id: int
    pos: Vector
    vel: Vector
    acc: Vector

    @classmethod
    def new(cls, i: int, s: str) -> Self:
        components: dict[str, Vector] = dict()
        for value in s.split(", "):
            name, vector = parse_vector(value)
            components[name] = vector
        return cls(id=i, pos=components["p"], vel=components["v"], acc=components["a"])

    def step(self):
        self.vel = add(self.vel, self.acc)
        self.pos = add(self.pos, self.vel)


@answer.timer
def main() -> None:
    lines = Parser().lines()
    answer.part1(161, run_simulation(lines, False)[0].id)
    answer.part2(438, len(run_simulation(lines, True)))


def run_simulation(lines: list[str], cleanup: bool) -> list[Particle]:
    particles = [Particle.new(i, line) for i, line in enumerate(lines)]
    for _ in range(1_000):
        seen: set[Vector] = set()
        bad_positions: set[Vector] = set()
        for particle in particles:
            particle.step()
            if cleanup:
                if particle.pos in seen:
                    bad_positions.add(particle.pos)
                else:
                    seen.add(particle.pos)

        delete_particles = [
            particle for particle in particles if particle.pos in bad_positions
        ]
        [particles.remove(particle) for particle in delete_particles]

    particles.sort(key=lambda particle: size(particle.pos))
    return particles


if __name__ == "__main__":
    main()
