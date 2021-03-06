import itertools

from commons.aoc_parser import Parser


def main():
    distances = get_distances()
    locations = get_locations(distances)

    options = []
    for permutation in itertools.permutations(locations):
        result = distance(permutation, distances)
        options.append(result)
        
    # Part 1: 141
    print('Part 1: {}'.format(min(options)))
    # Part 2: 736
    print('Part 2: {}'.format(max(options)))
    

def get_distances():
    distances = {}
    for line in Parser().lines():
        line = line.split()
        distances[(line[0], line[2])] = int(line[4])
        distances[(line[2], line[0])] = int(line[4])
    return distances


def get_locations(distances):
    locations = set()
    for key in distances.keys():
        locations.add(key[0])
        locations.add(key[1])
    return locations


def distance(locations, distances):
    result = []
    for i in range(1, len(locations)):
        leg = distances[(locations[i - 1], locations[i])]
        result.append(leg)
    return sum(result)


if __name__ == '__main__':
    main()
