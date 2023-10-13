from aoc import answer

PASSWORD_RANGE = 256_310, 732_736


class Password:
    def __init__(self, value):
        self.value = str(value)

    def valid(self, exact):
        ahead_same = self.same_counts()
        if exact:
            same_condition = 2 in ahead_same
        else:
            same_condition = any([same >= 2 for same in ahead_same])
        return same_condition and self.only_increase()

    def same_counts(self):
        ahead_same, i = [], 0
        while i < len(self.value):
            length = self.get_length_of_same(i)
            ahead_same.append(length)
            i += length
        return ahead_same

    def get_length_of_same(self, start):
        current, end = self.value[start], start
        while end < len(self.value) and self.value[end] == current:
            end += 1
        return end - start

    def only_increase(self):
        for i, digit in enumerate(self.value[:-1]):
            if int(digit) > int(self.value[i + 1]):
                return False
        return True


def main():
    answer.part1(979, get_num_valid(False))
    answer.part2(635, get_num_valid(True))


def get_num_valid(exact):
    are_valid = []
    for i in get_range():
        are_valid.append(Password(i).valid(exact))
    return sum(are_valid)


def get_range():
    return range(PASSWORD_RANGE[0], PASSWORD_RANGE[1] + 1)


if __name__ == "__main__":
    main()
