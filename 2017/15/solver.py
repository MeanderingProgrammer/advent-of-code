from dataclasses import dataclass

from aoc import answer


@dataclass
class Generator:
    value: int
    factor: int
    mult: int

    def next(self, wait_mult: bool) -> int:
        self.calculate()
        while wait_mult and self.value % self.mult != 0:
            self.calculate()
        return self.value

    def calculate(self) -> None:
        self.value *= self.factor
        self.value %= 2_147_483_647


def main() -> None:
    answer.part1(592, matches(40_000_000, False))
    answer.part2(320, matches(5_000_000, True))


def matches(n: int, wait_mult: bool) -> int:
    gen_a = Generator(value=277, factor=16_807, mult=4)
    gen_b = Generator(value=349, factor=48_271, mult=8)
    count = 0
    for _ in range(n):
        if equal(gen_a.next(wait_mult), gen_b.next(wait_mult)):
            count += 1
    return count


def equal(v1: int, v2: int) -> bool:
    v1_bin = bin(v1)[-16:]
    v2_bin = bin(v2)[-16:]
    return v1_bin == v2_bin


if __name__ == "__main__":
    main()
