from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class PasswordEntry:
    range_start: int
    range_end: int
    letter: str
    password: str

    def valid_v1(self) -> bool:
        letter_count = sum([letter == self.letter for letter in self.password])
        return letter_count >= self.range_start and letter_count <= self.range_end

    def valid_v2(self) -> bool:
        letter1 = self.password[self.range_start - 1]
        letter2 = self.password[self.range_end - 1]
        return (letter1 == self.letter) != (letter2 == self.letter)


def main() -> None:
    passwords = get_passwords()
    answer.part1(536, sum([password.valid_v1() for password in passwords]))
    answer.part2(558, sum([password.valid_v2() for password in passwords]))


def get_passwords() -> list[PasswordEntry]:
    def parse_password(line: str) -> PasswordEntry:
        parts = line.strip().split()
        value_range = parts[0].split("-")
        return PasswordEntry(
            range_start=int(value_range[0]),
            range_end=int(value_range[1]),
            letter=parts[1][:-1],
            password=parts[2],
        )

    return [parse_password(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
