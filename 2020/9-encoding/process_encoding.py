PREAMBLE_LENGTH = 25

class MaskingInput:

    def __init__(self, data):
        self.data = data


    def get_first_invalid(self):
        for i in range(PREAMBLE_LENGTH, len(self.data)):
            if not self.is_valid_index(i):
                return self.data[i]
        return None

    def is_valid_index(self, i):
        preamble = self.data[i-PREAMBLE_LENGTH:i]
        datum = self.data[i]
        return self.can_sum(preamble, datum)

    def get_sum_set(self, goal):
        for i in range(len(self.data)):
            for j in range(i+2, len(self.data)):
                subset = self.data[i:j]
                total = sum(subset)
                if total == goal:
                    return subset
                elif total > goal:
                    break
        return None


    @staticmethod
    def can_sum(preamble, datum):
        for value in preamble:
            needed = datum - value
            if needed in preamble:
                return True
        return False


def main():
    masking = MaskingInput(process())

    invalid_number = masking.get_first_invalid()
    print('Invalid number = {}'.format(invalid_number))

    sum_set = masking.get_sum_set(invalid_number)
    magic_number = min(sum_set) + max(sum_set)
    print('Break key = {}'.format(magic_number))


def process():
    data = []
    f = open('data.txt', 'r')

    for line in f:
        line = line.strip()
        data.append(int(line))

    f.close()
    return data


if __name__ == '__main__':
    main()

