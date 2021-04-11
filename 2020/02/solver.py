from commons.aoc_parser import Parser


class PasswordEntry:

    def __init__(self, raw_value):
        parts = raw_value.strip().split()

        value_range = parts[0].split('-')
        self.range_start =  int(value_range[0])
        self.range_end = int(value_range[1])

        self.letter = parts[1][:-1]

        self.password = parts[2]


    def valid_v1(self):
        letter_count = sum([letter == self.letter for letter in self.password])
        return letter_count >= self.range_start and letter_count <= self.range_end

    def valid_v2(self):
        letter1 = self.password[self.range_start - 1]
        letter2 = self.password[self.range_end -1]

        match1 = letter1 == self.letter
        match2 = letter2 == self.letter

        return match1 != match2


def main():
    passwords = get_passwords()
    # Part 1: 536
    print('Part 1: {}'.format(sum([password.valid_v1() for password in passwords])))
    # Part 2: 558
    print('Part 2: {}'.format(sum([password.valid_v2() for password in passwords])))


def get_passwords():
    return [PasswordEntry(line) for line in Parser().lines()]


if __name__ == '__main__':
    main()
