from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Masking:
    values: list[int]
    preamble: int

    def first_invalid(self) -> int:
        for i in range(self.preamble, len(self.values)):
            if not self.can_sum(i):
                return self.values[i]
        raise Exception("Failed")

    def can_sum(self, i: int) -> bool:
        target: int = self.values[i]
        preamble: list[int] = self.values[i - self.preamble : i]
        for value in preamble:
            if target - value in preamble:
                return True
        return False

    def get_sum_set(self, target: int) -> list[int]:
        for i in range(len(self.values)):
            for j in range(i + 1, len(self.values)):
                subset = self.values[i:j]
                total = sum(subset)
                if total == target:
                    return subset
                elif total > target:
                    break
        raise Exception("Failed")


@answer.timer
def main() -> None:
    masking = Masking(values=Parser().int_lines(), preamble=25)
    invalid_number = masking.first_invalid()
    answer.part1(104054607, invalid_number)
    sum_set = masking.get_sum_set(invalid_number)
    answer.part2(13935797, min(sum_set) + max(sum_set))


if __name__ == "__main__":
    main()
