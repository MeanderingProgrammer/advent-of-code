from collections import defaultdict

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class Particle:

    def __init__(self, value):
        self.id = value[0]
        values = value[1].split(', ')

        components = {}
        for value in values:
            value = value.split('=')
            
            name = value[0]
            value = value[1][1:-1]
            value = [int(val) for val in value.split(',')]
            components[name] = Point(*value)

        self.pos = components['p']
        self.vel = components['v']
        self.acc = components['a']

    def step(self):
        self.vel += self.acc
        self.pos += self.vel

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: p={}, v={}, a={}'.format(self.id, self.pos, self.vel, self.acc)


def main():
    # Part 1: 161
    particles = run_simulation(False)
    print('Long-term closest = {}'.format(particles[0].id))
    # Part 2: 438
    particles = run_simulation(True)
    print('Remaining particles = {}'.format(len(particles)))


def run_simulation(cleanup):
    particles = get_particles()
    for i in range(1_000):
        seen = set()
        to_remove = set()

        for particle in particles:
            particle.step()
            pos = particle.pos

            if pos in seen:
                if cleanup:
                    to_remove.add(pos)
            else:
                seen.add(pos)


        delete_particles = set()
        for particle in particles:
            if particle.pos in to_remove:
                delete_particles.add(particle)

        for delete_particle in delete_particles:
            particles.remove(delete_particle)

    particles.sort(key=lambda particle: len(particle.pos))
    return particles

def get_particles():
    return [Particle(line) for line in enumerate(Parser(FILE_NAME).lines())]


if __name__ == '__main__':
    main()

