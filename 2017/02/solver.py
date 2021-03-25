from aoc_parser import Parser


FILE_NAME = 'data'


def main():
    # Part 1: 47623
    print('Part 1: {}'.format(calculate_checksum(checksum_v1)))
    # Part 2: 312
    print('Part 2: {}'.format(calculate_checksum(checksum_v2)))


def calculate_checksum(f):
    checksums = []
    for line in Parser(FILE_NAME).lines():
        values = [int(value) for value in line.split()]
        checksum = f(values)
        checksums.append(checksum)
    return sum(checksums)


def checksum_v1(values):
    return max(values) - min(values)


def checksum_v2(values):
    for i, v1 in enumerate(values[:-1]):
        for v2 in values[i + 1:]:
            num = max(v1, v2)
            denom = min(v1, v2)
            if num % denom == 0:
                return num // denom


if __name__ == '__main__':
    main()
