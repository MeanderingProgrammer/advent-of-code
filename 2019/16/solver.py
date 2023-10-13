from aoc import answer
from aoc.parser import Parser


class Transmission:
    def __init__(self, raw, apply_offset):
        self.digits = [int(value) for value in raw]
        self.apply_offset = apply_offset
        if self.apply_offset:
            offset = self.first_n(7)
            self.digits = self.digits[offset:]

    def forward(self):
        if self.apply_offset:
            self.digits = self.forward_with_offset()
        else:
            self.digits = self.forward_from_start()

    def forward_from_start(self):
        return [self.get_new_digit(i) for i in range(len(self.digits))]

    def get_new_digit(self, i):
        pattern, pattern_index = self.get_pattern(i + 1), 1
        new_digit = 0
        for digit in self.digits:
            new_digit += pattern[pattern_index % len(pattern)] * digit
            pattern_index += 1
        return abs(new_digit) % 10

    def forward_with_offset(self):
        # Going from back to front each digit is the
        # current sum % 10
        # This only applies in the middle of a set
        # of digits and does not hold to the start
        self.digits.reverse()

        new_digits, current_sum = [], 0
        for digit in self.digits:
            current_sum += digit
            new_digits.append(current_sum % 10)
        new_digits.reverse()

        return new_digits

    def first_n(self, n):
        first_n_digits = [str(digit) for digit in self.digits[:n]]
        as_string = "".join(first_n_digits)
        return int(as_string)

    @staticmethod
    def get_pattern(length):
        components = [[0] * length, [1] * length, [0] * length, [-1] * length]
        return [value for component in components for value in component]


def main():
    answer.part1(77038830, apply_fft(1, False))
    answer.part2(28135104, apply_fft(10_000, True))


def apply_fft(repeats, apply_offset):
    transmission = get_transmission(repeats, apply_offset)
    for i in range(100):
        transmission.forward()
    return transmission.first_n(8)


def get_transmission(repeats, apply_offset):
    return Transmission(Parser().string() * repeats, apply_offset)


if __name__ == "__main__":
    main()
