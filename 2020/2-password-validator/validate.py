class PasswordEntry:

    def __init__(self, raw_value):
        parts = raw_value.strip().split()

        expected_count = parts[0].split('-')
        self.index1 = int(expected_count[0]) - 1
        self.index2 = int(expected_count[1]) - 1

        self.letter = parts[1][:-1]

        self.password = parts[2]

    def is_valid(self):
        letter1 = self.password[self.index1]
        letter2 = self.password[self.index2]

        match1 = letter1 == self.letter
        match2 = letter2 == self.letter
        return match1 != match2


def main():
    f = open('data.txt', 'r')
    num_valid = 0
    
    for line in f:
        entry = PasswordEntry(line)
        if entry.is_valid():
            num_valid += 1

    print('Total valid entries = {}'.format(num_valid))
    f.close()


if __name__ == '__main__':
    main()
