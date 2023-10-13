import hashlib
from aoc import answer


SALT = "qzyelonm"


def main():
    answer.part1(15168, generate_keys(64, 1))
    answer.part2(20864, generate_keys(64, 2_017))


def generate_keys(n, num_hashes):
    keys = set()

    i, hash_data = 1, {}
    while len(keys) < n + 5:
        value = SALT + str(i)
        hashed = hash(value, num_hashes)
        triples = get_repeats(hashed, 3)
        cinqs = get_repeats(hashed, 5)
        if len(triples) > 0:
            hash_data[i] = triples[0]
            for cinq in cinqs:
                matches = get_matches(i, cinq, hash_data)
                for match in matches:
                    keys.add(match)
        i += 1

    keys = list(keys)
    keys.sort()
    return keys[n - 1]


def hash(value, n):
    for i in range(n):
        value = hashlib.md5(str.encode(value)).hexdigest()
    return value


def get_repeats(hashed, length):
    repeats = []
    for i in range(len(hashed) - length + 1):
        value = hashed[i : i + length]
        if all_same(value):
            repeats.append(value[0])
    return repeats


def all_same(value):
    return len(set([v for v in value])) == 1


def get_matches(i, cinq, hash_data):
    matches = []
    for ii in range(i - 1_000, i):
        if ii in hash_data:
            if hash_data[ii] == cinq:
                matches.append(ii)
    return matches


if __name__ == "__main__":
    main()
