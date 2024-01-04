from collections import deque
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass
class Knot:
    q: deque[int]
    lengths: list[int]
    skip_size: int
    skipped: int

    def run(self) -> None:
        for length in self.lengths:
            temp = [self.q.popleft() for _ in range(length)]
            temp.reverse()

            self.q.extend(temp)
            self.q.rotate(-self.skip_size)

            self.skipped += length + self.skip_size
            self.skip_size += 1

    def score(self) -> int:
        self.q.rotate(self.skipped)
        return self.q.popleft() * self.q.popleft()

    def dense_hash(self) -> str:
        self.q.rotate(self.skipped)
        as_list: list[int] = list(self.q)
        hashed: str = ""
        for i in range(0, len(as_list), 16):
            hashed += Knot.hash_block(as_list[i : i + 16])
        return hashed

    @staticmethod
    def hash_block(values: list[int]) -> str:
        hashed = 0
        for value in values:
            hashed ^= value
        hex_value = hex(hashed)[2:]
        return hex_value if len(hex_value) == 2 else "0" + hex_value


@answer.timer
def main() -> None:
    knot = run_knot(False, [], 1)
    answer.part1(38415, knot.score())
    knot = run_knot(True, [17, 31, 73, 47, 23], 64)
    answer.part2("9de8846431eef262be78f590e39a4848", knot.dense_hash())


def run_knot(use_ord: bool, additional: list[int], times: int) -> Knot:
    lengths = Parser().ord_string() if use_ord else Parser().int_csv()
    knot = Knot(
        q=deque(range(256)),
        lengths=lengths + additional,
        skip_size=0,
        skipped=0,
    )
    for _ in range(times):
        knot.run()
    return knot


if __name__ == "__main__":
    main()
