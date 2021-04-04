from collections import deque


NUM_ELVES = 3_014_603


def main():
    # Part 1: 1834903
    print('Part 1: {}'.format(solve_by_pattern(True)))
    # Part 2: 1420280
    print('Part 2: {}'.format(solve_by_pattern(False)))


def solve_by_pattern(always_increment):
    winning_elve = 1
    for i in range(1, NUM_ELVES + 1):
        winning_elve += 1
        if always_increment or winning_elve > i // 2:
            winning_elve += 1

        if winning_elve > i:
            winning_elve = 1
    return winning_elve


# This function is used to find the patterns implemented in
# solve_by_pattern. It is not needed after the patterns are
# found but leaving it here for reference.
def get_patterns():
    # Part 1 pattern is the winning elve inceases by 2
    # for each elve we add. If the winning elve ends up
    # being larger than the total number of elves we start
    # the pattern over.
    run_for_pattern(location_v1)
    # Part 2 pattern is the winning elve inceases by 1
    # for each elve we add. If the winning elve is 
    # greater than half of the total number of elves we instead 
    # increase by 2. We roll over to back to 1 same as Part 1.
    run_for_pattern(location_v2)


def run_for_pattern(location):
    for i in range(1, 100):
        print(i, run_with_n(location, i))


def run_with_n(location, n):
    elves, elves_left = get_start_state(n)

    while elves_left > 1:
        del elves[location(elves_left)]
        elves_left -= 1
        elves.rotate(-1)

    return elves[0] + 1


def location_v1(elves_left):
    return 1


def location_v2(elves_left):
    return elves_left // 2


def get_start_state(n):
    return deque(range(n)), n


if __name__ == '__main__':
    main()
