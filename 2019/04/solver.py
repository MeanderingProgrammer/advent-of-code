from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True, slots=True)
class Password:
    value: str

    def only_increase(self) -> bool:
        for i in range(len(self.value) - 1):
            if int(self.value[i]) > int(self.value[i + 1]):
                return False
        return True

    def valid_p1(self) -> bool:
        return any([same >= 2 for same in self.same_counts()])

    def valid_p2(self) -> bool:
        return 2 in self.same_counts()

    def same_counts(self) -> list[int]:
        ahead_same, i = [], 0
        while i < len(self.value):
            length = self.get_length_of_same(i)
            ahead_same.append(length)
            i += length
        return ahead_same

    def get_length_of_same(self, start: int) -> int:
        current, end = self.value[start], start
        while end < len(self.value) and self.value[end] == current:
            end += 1
        return end - start


@answer.timer
def main() -> None:
    start, end = Parser().string().split("-")
    passwords = [Password(str(i)) for i in range(int(start), int(end) + 1)]
    passwords = [password for password in passwords if password.only_increase()]
    answer.part1(979, sum([password.valid_p1() for password in passwords]))
    answer.part2(635, sum([password.valid_p2() for password in passwords]))


if __name__ == "__main__":
    main()
