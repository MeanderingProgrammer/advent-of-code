from aoc import answer
from aoc.parser import Parser


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
    answer.part1(6782, sum([group.any_positive() for group in groups]))
    answer.part2(3596, sum([group.all_positive() for group in groups]))


def process():
    return [BoardingGroup(group) for group in Parser().line_groups()]


if __name__ == "__main__":
    main()
