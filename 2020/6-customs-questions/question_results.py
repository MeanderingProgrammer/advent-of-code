class BoardingGroup:

    def __init__(self, responders):
        self.responders = responders

    def count_all_positive(self):
        positive_responses = set(self.responders[0])
        for i in range(1, len(self.responders)):
            responder = self.responders[i]
            positives = set(responder)
            positive_responses = positive_responses.intersection(positives)
        return len(positive_responses)


def main():
    data = process()
    groups = group_data(data)

    total_positive = 0
    for group in groups:
        group = BoardingGroup(group)
        positive_responses = group.count_all_positive()
        total_positive += positive_responses
    print('Total positive responses = {}'.format(total_positive))


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
    return groups

if __name__ == '__main__':
    main()

