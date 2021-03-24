class Transmission:

    def __init__(self, raw, repeats, n):
        self.value = [int(value) for value in raw] * repeats
        if n is not None:
            self.value = self.value[self.get_digits(n):]
    
    def forward(self):
        value = [v for v in self.value]
        value.reverse()

        total = 0
        new_value = []
        for v in value:
            total += v
            new_value.append(total % 10)
        new_value.reverse()

        self.value = new_value

    def get_digits(self, n):
        digits = self.value[:n]
        value = ''.join([str(digit) for digit in digits])
        return int(value)


def main():
    #solve_part_1()
    solve_part_2()

def solve_part_1():
    # Part 1 = 77038830
    # No longer works for part 1 :(
    transmission = get_transmission(1, None)
    print(transmission.value)
    for i in range(100):
        transmission.forward()
        print(transmission.value)
    print('First 8 digits = {}'.format(transmission.get_digits(8)))


def solve_part_2():
    # Part 2 = 28135104
    transmission = get_transmission(10_000, 7)
    for i in range(100):
        transmission.forward()
    print('8 digits from offset = {}'.format(transmission.get_digits(8)))


def get_transmission(repeats, n):
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return Transmission(f.read(), repeats, n)


if __name__ == '__main__':
    main()
