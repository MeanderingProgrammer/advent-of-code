from commons.aoc_parser import Parser


class Dance:

    def __init__(self, length):
        self.dancers = [chr(ord('a') + i) for i in range(length)]

    def spin(self, n):
        self.dancers = self.dancers[-n:] + self.dancers[:-n]

    def exchange(self, index1, index2):
        temp = self.dancers[index1]
        self.dancers[index1] = self.dancers[index2]
        self.dancers[index2] = temp

    def partner(self, p1, p2):
        index1 = self.dancers.index(p1)
        index2 = self.dancers.index(p2)
        self.exchange(index1, index2)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ''.join(self.dancers)


def main():
    dance = Dance(16)
    moves = get_moves()
    pattern = get_pattern(dance, moves)

    # Part 1: eojfmbpkldghncia
    print('Part 1: {}'.format(pattern[1]))
    # Part 2: iecopnahgdflmkjb
    index = 1_000_000_000 % len(pattern)
    print('Part 2: {}'.format(pattern[index]))


def get_pattern(dance, moves):
    # Pattern happens to repeat from start immediately once we see
    # a value that is the same
    pattern = []
    while str(dance) not in pattern:
        pattern.append(str(dance))
        perform_dance(dance, moves)
    return pattern


def perform_dance(dance, moves):
    for move in moves:
        op = move[0]
        args = move[1:]
        if op == 's':
            dance.spin(int(args))
        elif op == 'x':
            indexes = args.split('/')
            dance.exchange(int(indexes[0]), int(indexes[1]))
        elif op == 'p':
            parners = args.split('/')
            dance.partner(parners[0], parners[1])
        else:
            raise Exception('Unkown operation: {}'.format(op))


def get_moves():
    return Parser().csv()


if __name__ == '__main__':
    main()
