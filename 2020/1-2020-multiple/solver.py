def main():
    values = read_data()
    triple = find_triple(values)
    print('The three values are {}, {}, and {}'.format(triple[0], triple[1], triple[2]))
    print('Multiplied = {}'.format(triple[0] * triple[1] * triple[2]))


def read_data():
    data = []
    f = open('data.txt', 'r')
    
    for line in f:
        data.append(int(line.strip()))
    
    f.close()
    return data

def find_triple(values):
    ignore = set()
    for value in values:
        needed = 2020 - value
        ignore.add(value)
        # Remove value from values
        pair = find_pair(needed, values, ignore)
        if pair is not None:
            return (value, pair[0], pair[1])


def find_pair(goal, values, ignore):
    for value in values:
        if value not in ignore:
            needed = goal - value
            if needed in values:
                return (value, needed)
    return None


if __name__ == '__main__':
    main()
