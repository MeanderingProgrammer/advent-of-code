import math


class Vector:

    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def simplify(self):
        return Vector(
            self.simple_component(self.x),
            self.simple_component(self.y),
            self.simple_component(self.z)
        )

    def simple_component(self, value):
        if value < 0:
            return 1
        elif value > 0:
            return -1
        else:
            return 0

    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __add__(self, other):
        dx = self.x + other.x
        dy = self.y + other.y
        dz = self.z + other.z
        return Vector(dx, dy, dz)

    def __sub__(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return Vector(dx, dy, dz)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<x={}, y={}, z={}>'.format(self.x, self.y, self.z)


class Body:

    def __init__(self, raw):
        raw = raw[1:-1]
        parts = raw.split(', ')
        parts = [int(part.split('=')[1]) for part in parts]
        self.position = Vector(*parts)
        self.velocity = Vector()

    def add_gravity(self, other):
        difference = self.position - other.position
        gravity = difference.simplify()
        self.velocity += gravity

    def apply_velocity(self):
        self.position += self.velocity

    def energy(self):
        return self.position.energy() * self.velocity.energy()

    def extract(self, extractor):
        return extractor(self.position), extractor(self.velocity)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'pos = {}, vel ={}'.format(self.position, self.velocity)


class System:

    def __init__(self):
        self.bodies = []

    def add(self, body):
        self.bodies.append(body)

    def step(self):
        for body in self.bodies:
            others = [other for other in self.bodies if other != body]
            for other in others:
                body.add_gravity(other)
        [body.apply_velocity() for body in self.bodies]

    def energy(self):
        body_energies = [body.energy() for body in self.bodies]
        return sum(body_energies)

    def extract(self, extractor):
        return [body.extract(extractor) for body in self.bodies]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join([str(body) for body in self.bodies])


def main():
    # Part 1: 5350
    print('Part 1: {}'.format(run_for(1_000)))
    # Part 2: 467034091553512
    print('Part 2: {}'.format(get_system_period()))


def run_for(n):
    system = get_system()
    for i in range(n):
        system.step()
    return system.energy()


def get_system_period():
    x_period = component_period(lambda vector: vector.x)
    y_period = component_period(lambda vector: vector.y)
    z_period = component_period(lambda vector: vector.z)

    return lcm(lcm(x_period, y_period), z_period)


def component_period(extractor):
    goal_state = get_system().extract(extractor)

    system, step = get_system(), 1
    system.step()

    while system.extract(extractor) != goal_state:
        system.step()
        step += 1

    return step


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def get_system():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().split('\n')

    system = System()
    [system.add(Body(datum)) for datum in data]
    return system


if __name__ == '__main__':
    main()
