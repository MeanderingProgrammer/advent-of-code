from collections import defaultdict


class Orbits:

    def __init__(self):
        self.orbits = defaultdict(list)

    def add(self, orbit):
        orbit = orbit.split(')')
        self.orbits[orbit[0]].append(orbit[1])

    def get_distance(self, start, finish):
        explored = set()
        to_explore = [(start, -1)]

        for orbit, value in to_explore:
            for adjacent in self.get_adjacent(orbit):
                if adjacent == finish:
                    return value
                elif adjacent not in explored:
                    to_explore.append((adjacent, value+1))
            explored.add(orbit)


    def get_adjacent(self, node):
        adjacent = [value for value in self.orbits[node]]
        for k, v in self.orbits.items():
            if node in v:
                adjacent.append(k)
        return adjacent

    def __len__(self):
        count = 0

        to_explore = [('COM', 0)]
        for orbit, value in to_explore:
            count += value
            for adjacent in self.orbits[orbit]:
                to_explore.append((adjacent, value+1))

        return count

    def __str__(self):
        return str(self.orbits)


def main():
    orbits = get_orbits()
    # Part 1 = 358244
    print('Total # of orbits = {}'.format(len(orbits)))
    # Part 2 = 
    print('Distance = {}'.format(orbits.get_distance('YOU', 'SAN')))


def get_orbits():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().split('\n')

    orbits = Orbits()
    for orbit in data:
        orbits.add(orbit)
    return orbits


if __name__ == '__main__':
    main()

