from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class MaskingInput:
    data: list[int]
    preamble_length: int

    def first_invalid(self) -> int:
        for i in range(self.preamble_length, len(self.data)):
            if not self.can_sum(i):
                return self.data[i]
        raise Exception("Failed")

    def can_sum(self, i: int) -> bool:
        preamble: list[int] = self.data[i - self.preamble_length : i]
        datum: int = self.data[i]
        for value in preamble:
            if datum - value in preamble:
                return True
        return False

    def get_sum_set(self, goal: int) -> list[int]:
        for i in range(len(self.data)):
            for j in range(i + 1, len(self.data)):
                subset = self.data[i:j]
                total = sum(subset)
                if total == goal:
                    return subset
                elif total > goal:
                    break
        raise Exception("Failed")


@answer.timer
def main() -> None:
    masking = MaskingInput(data=Parser().int_lines(), preamble_length=25)
    invalid_number = masking.first_invalid()
    answer.part1(104054607, invalid_number)
    sum_set = masking.get_sum_set(invalid_number)
    answer.part2(13935797, min(sum_set) + max(sum_set))


if __name__ == "__main__":
    main()
