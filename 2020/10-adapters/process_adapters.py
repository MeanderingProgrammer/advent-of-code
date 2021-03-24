from collections import defaultdict


class Adapters:

    def __init__(self, data):
        self.data = sorted(data)
        # Add starting point
        self.data.insert(0, 0)
        # Add ending point
        self.data.append(self.data[-1] + 3)

    def get_chains(self):
        chains = defaultdict(int)
        for i in range(1, len(self.data)):
            current = self.data[i]
            previous = self.data[i-1]
            difference = current - previous
            chains[difference] += 1
        return chains

    def get_num_combinations(self):
        num_paths = []
        for i in range(len(self.data)-1):
            num_paths.append(self.get_num_paths(i))

        for i in range(len(num_paths) - 2, -1, -1):
            paths = num_paths[i]
            num_paths[i] = 0
            for j in range(i + 1, i + 1 + paths):
                num_paths[i] += num_paths[j]
        return num_paths[0]

    def get_num_paths(self, i):
        current = self.data[i]
        max_value = self.data[i] + 3
        next_adapters = [adapter for adapter in self.data if adapter > current and adapter <= max_value]
        return len(next_adapters)


def main():
    adapters = Adapters(process())
    # Part 1 = 2343
    chains = adapters.get_chains()
    print('Magic number = {}'.format(chains[1] * chains[3]))
    # Part 2 = 31581162962944
    num_combinations = adapters.get_num_combinations()
    print('Total number of combinations = {}'.format(num_combinations))


def process():
    with open('data.txt', 'r') as f:
        return [int(line) for line in f.read().splitlines()]


if __name__ == '__main__':
    main()

