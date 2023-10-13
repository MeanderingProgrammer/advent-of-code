import collections
from aoc import answer
from aoc.parser import Parser


class Knot:
    def __init__(self, size, lengths):
        self.q = collections.deque(range(size))
        self.lengths = lengths

        self.skip_size = 0
        self.skipped = []

    def run_hash(self, times=1):
        for time in range(times):
            self.run_once()

    def run_once(self):
        for length in self.lengths:
            temp = [self.q.popleft() for i in range(length)]
            temp.reverse()

            self.q.extend(temp)
            self.q.rotate(-self.skip_size)

            self.skipped.append(length + self.skip_size)
            self.skip_size += 1

    def rotate_back(self):
        self.q.rotate(sum(self.skipped))

    def score(self):
        self.rotate_back()
        return self.q.popleft() * self.q.popleft()

    def dense_hash(self):
        hashed = []

        self.rotate_back()
        as_list = list(self.q)
        for i in range(len(as_list) // 16):
            start = i * 16
            end = start + 16
            block = as_list[start:end]
            hashed.append(self.hash_block(block))

        return "".join(hashed)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.q)

    @staticmethod
    def hash_block(values):
        hashed = 0
        for value in values:
            hashed ^= value
        hex_value = hex(hashed)[2:]
        return hex_value if len(hex_value) == 2 else "0" + hex_value


def main():
    size = 256

    knot = Knot(size, get_lengths(False))
    knot.run_hash()
    answer.part1(38415, knot.score())

    knot = Knot(size, get_lengths(True) + [17, 31, 73, 47, 23])
    knot.run_hash(64)
    answer.part2("9de8846431eef262be78f590e39a4848", knot.dense_hash())


def get_lengths(to_ord):
    parser = Parser()
    return parser.ord_string() if to_ord else parser.int_csv()


if __name__ == "__main__":
    main()
