from dataclasses import dataclass

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

    def step(self):
        self.vel = add(self.vel, self.acc)
        self.pos = add(self.pos, self.vel)


@answer.timer
def main() -> None:
    answer.part1(161, run_simulation(False)[0].id)
    answer.part2(438, len(run_simulation(True)))


def run_simulation(cleanup: bool) -> list[Particle]:
    def parse_particle(i: int, line: str) -> Particle:
        components: dict[str, Vector] = dict()
        for value in line.split(", "):
            name, vector = parse_vector(value)
            components[name] = vector
        return Particle(
            id=i, pos=components["p"], vel=components["v"], acc=components["a"]
        )

    particles = [parse_particle(i, line) for i, line in enumerate(Parser().lines())]
    for _ in range(1_000):
        seen, to_remove = set(), set()
        for particle in particles:
            particle.step()
            if particle.pos in seen:
                if cleanup:
                    to_remove.add(particle.pos)
            else:
                seen.add(particle.pos)

        delete_particles = [
            particle for particle in particles if particle.pos in to_remove
        ]
        [particles.remove(particle) for particle in delete_particles]

    particles.sort(key=lambda particle: size(particle.pos))
    return particles


if __name__ == "__main__":
    main()
