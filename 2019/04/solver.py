class Password:

    def __init__(self, value):
        self.value = str(value)

    def valid(self):
        return self.adjacent_same() and self.only_increase()

    def adjacent_same(self):
        matches = []
        look_ahead = self.value[:-1]
        for i, digit in enumerate(look_ahead):
            match_length = 0
            for j, next_digit in enumerate(self.value[i:]):
                if next_digit != digit:
                    break
                match_length += 1
            if match_length == 2 and (len(matches) == 0 or matches[-1] == 1):
                return True
            matches.append(match_length)
        return False

    def only_increase(self):
        for i, digit in enumerate(self.value[:-1]):
            if int(digit) > int(self.value[i+1]):
                return False
        return True

def main():
    valid = 0
    for i in get_range():
        if Password(i).valid():
            valid += 1
    print('Total possible = {}'.format(valid))


def get_range():
    minimum = 256310
    maximum = 732736
    return range(minimum, maximum + 1)

if __name__ == '__main__':
    main()

