from collections import deque


NUM_ELVES = 3_014_603


def main():
    # Part 1: 1834903
    print('Part 1: {}'.format(run(location_v1)))
    # Part 2: 1420280
    print('Part 2: {}'.format(run(location_v2)))


def run(location):
    elves, elves_left = get_start_state()

    while elves_left > 1:
        del elves[location(elves_left)]
        elves.rotate(-1)
        elves_left -= 1

    return elves[0] + 1


def location_v1(elves_left):
    return 1


def location_v2(elves_left):
    return elves_left // 2


def get_start_state():
    return deque(range(NUM_ELVES)), NUM_ELVES


if __name__ == '__main__':
    main()
