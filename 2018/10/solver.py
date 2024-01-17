import re
from dataclasses import dataclass

from aoc import answer
from aoc.grid import Grid, GridHelper
from aoc.parser import Parser
from aoc.point import Point, PointHelper


@dataclass(frozen=True)
class Particle:
    position: Point
    velocity: Point

    def at(self, time: int) -> Point:
        return PointHelper.add(self.position, PointHelper.multiply(self.velocity, time))


@dataclass(frozen=True)
class Particles:
    particles: list[Particle]

    def area_at(self, time: int) -> int:
        positions = [particle.at(time) for particle in self.particles]
        xs = [x for x, _ in positions]
        ys = [y for _, y in positions]
        return (max(ys) - min(ys)) * (max(xs) - min(xs))

    def grid_str(self, time: int) -> str:
        grid: Grid[str] = dict()
        for particle in self.particles:
            x, y = particle.at(time)
            grid[(x, -y)] = "#"
        return GridHelper.to_str(grid)


@answer.timer
def main() -> None:
    particles = get_particles()
    time = min_area(particles)
    expected = [
        ".####...#####......###..#.......#.......#.......#.......#....#",
        "#....#..#....#......#...#.......#.......#.......#.......#....#",
        "#.......#....#......#...#.......#.......#.......#.......#....#",
        "#.......#....#......#...#.......#.......#.......#.......#....#",
        "#.......#####.......#...#.......#.......#.......#.......######",
        "#..###..#...........#...#.......#.......#.......#.......#....#",
        "#....#..#...........#...#.......#.......#.......#.......#....#",
        "#....#..#.......#...#...#.......#.......#.......#.......#....#",
        "#...##..#.......#...#...#.......#.......#.......#.......#....#",
        ".###.#..#........###....######..######..######..######..#....#",
    ]
    answer.part1("\n" + "\n".join(expected), "\n" + particles.grid_str(time))
    answer.part2(10515, time)


def min_area(particles: Particles) -> int:
    previous_area, time = particles.area_at(0), 0
    while True:
        next_area = particles.area_at(time + 1)
        if next_area > previous_area:
            return time
        previous_area = next_area
        time += 1


def get_particles() -> Particles:
    particles = []
    pattern = "^position=<(.*), (.*)> velocity=<(.*), (.*)>$"
    for line in Parser().lines():
        match = re.match(pattern, line)
        if match is None:
            raise Exception(f"Cannot parse: {line}")
        particle = Particle(
            position=(int(match[1]), int(match[2])),
            velocity=(int(match[3]), int(match[4])),
        )
        particles.append(particle)
    return Particles(particles=particles)


if __name__ == "__main__":
    main()
