from aoc import answer
from aoc.parser import Parser


def main():
    answer.part1(47623, calculate_checksum(checksum_v1))
    answer.part2(312, calculate_checksum(checksum_v2))


def calculate_checksum(f):
    checksums = []
    for line in Parser().lines():
        values = [int(value) for value in line.split()]
        checksum = f(values)
        checksums.append(checksum)
    return sum(checksums)


def checksum_v1(values):
    return max(values) - min(values)


def checksum_v2(values):
    for i, v1 in enumerate(values[:-1]):
        for v2 in values[i + 1 :]:
            num = max(v1, v2)
            denom = min(v1, v2)
            if num % denom == 0:
                return num // denom


if __name__ == "__main__":
    main()
