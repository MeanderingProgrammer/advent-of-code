from commons.aoc_parser import Parser


class BoardingGroup:

    def __init__(self, responders):
        self.responders = responders

    def any_positive(self):
        positive_responses = set(self.responders[0])
        for responder in self.responders[1:]:
            positive_responses |= set(responder)
        return len(positive_responses)

    def all_positive(self):
        positive_responses = set(self.responders[0])
        for responder in self.responders[1:]:
            positive_responses &= set(responder)
        return len(positive_responses)


def main():
    groups = process()
    # Part 1: 6782
    print('Part 1: {}'.format(sum([group.any_positive() for group in groups])))
    # Part 2: 3596
    print('Part 2: {}'.format(sum([group.all_positive() for group in groups])))


def process():
    return [BoardingGroup(group) for group in Parser().line_groups()]


if __name__ == '__main__':
    main()
