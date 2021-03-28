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
    groups = group_data(process())
    # Part 1: 6782
    print('Part 1: {}'.format(sum([group.any_positive() for group in groups])))
    # Part 2: 3596
    print('Part 2: {}'.format(sum([group.all_positive() for group in groups])))


def process():
    f = open('data.txt', 'r')
    data = f.readlines()
    f.close()
    data = [datum.strip() for datum in data]
    return data


def group_data(data):
    groups = []
    current_group = []
    for datum in data:
        if len(datum) == 0:
            groups.append(current_group)
            current_group = []
        else:
            current_group.append(datum)
    groups.append(current_group)
    return [BoardingGroup(group) for group in groups]


if __name__ == '__main__':
    main()
