from aoc_parser import Parser


FILE_NAME = 'data'


class Disk:

    def __init__(self, id, positions, start):
        self.id = id
        self.positions = positions
        self.start = start

    def passes(self, time):
        position = time + self.id + self.start
        return position % self.positions == 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '({}, {}, {})'.format(self.id, self.positions, self.start)


def main():
    # Part 1: 121834
    print('Part 1: {}'.format(calculate_first_pass(False)))
    # Part 2: 3208099
    print('Part 2: {}'.format(calculate_first_pass(True)))


def calculate_first_pass(add_disk):
    disks = get_disks()
    if add_disk:
        disks.append(Disk(
            len(disks) + 1,
            11,
            0
        ))

    passed, time = False, 0
    while not passed:
        time += 1
        passed = passes_all(disks, time)
    return time


def passes_all(disks, time):
    for disk in disks:
        if not disk.passes(time):
            return False
    return True


def get_disks():
    disks = []
    for line in Parser(FILE_NAME).lines():
        line = line.split()
        disks.append(Disk(
            int(line[1][1:]),
            int(line[3]),
            int(line[11][:-1])
        ))
    return disks


if __name__ == '__main__':
    main()
