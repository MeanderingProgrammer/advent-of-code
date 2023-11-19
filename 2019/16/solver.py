from aoc import answer
from aoc.parser import Parser

PATTERN = [0, 1, 0, -1]


class Transmission:
    def __init__(self, raw: str, apply_offset: bool):
        self.digits = [int(value) for value in raw]
        if apply_offset:
            self.digits = self.digits[self.first_n(7) :]

    def start(self) -> None:
        self.digits = [self.get_new_digit(i) for i in range(len(self.digits))]

    def get_new_digit(self, i: int) -> int:
        pattern_index, new_digit = 0, 0
        for digit in self.digits:
            pattern_index += 1
            new_digit += PATTERN[(pattern_index // (i + 1)) % len(PATTERN)] * digit
        return abs(new_digit) % 10

    def offset(self) -> None:
        # Going from back to front each digit is the current sum % 10
        # This only applies in the middle of a set of digits and does not hold to the start
        new_digits, current_sum = [], 0
        for digit in reversed(self.digits):
            current_sum += digit
            new_digits.append(current_sum % 10)
        new_digits.reverse()
        self.digits = new_digits

    def first_n(self, n: int) -> int:
        first_n_digits = [str(digit) for digit in self.digits[:n]]
        as_string = "".join(first_n_digits)
        return int(as_string)


def main() -> None:
    answer.part1(77038830, apply_fft(1, False))
    answer.part2(28135104, apply_fft(10_000, True))


def apply_fft(repeats: int, apply_offset: bool) -> int:
    transmission = Transmission(Parser().string() * repeats, apply_offset)
    for _ in range(100):
        if not apply_offset:
            transmission.start()
        else:
            transmission.offset()
    return transmission.first_n(8)


if __name__ == "__main__":
    main()
