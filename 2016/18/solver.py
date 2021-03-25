STARTING_ROW = '.^^^.^.^^^.^.......^^.^^^^.^^^^..^^^^^.^.^^^..^^.^.^^..^.^..^^...^.^^.^^^...^^.^.^^^..^^^^.....^....'

TRAP = '^'
SAFE = '.'


def main():
    # Part 1: 2013
    print('Part 1: {}'.format(total_safe(40)))
    # Part 2: 20006289
    print('Part 2: {}'.format(total_safe(400_000)))


def total_safe(n):
    rows = [STARTING_ROW]
    while len(rows) < n:
        next_row = get_next_row(rows[-1])
        rows.append(next_row)
    return count_safe(rows)


def get_next_row(previous_row):
    next_row = []
    for i in range(len(previous_row)):
        left = previous_row[i - 1] if i > 0 else SAFE
        center = previous_row[i]
        right = previous_row[i + 1] if i < len(previous_row) - 1 else SAFE
        element = get_element(left, center, right)
        next_row.append(element)
    return ''.join(next_row)


def get_element(left, center, right):
    possible_trap = [
        left == TRAP and center == TRAP and right == SAFE,
        left == SAFE and center == TRAP and right == TRAP,
        left == TRAP and center == SAFE and right == SAFE,
        left == SAFE and center == SAFE and right == TRAP
    ]
    return TRAP if any(possible_trap) else SAFE


def count_safe(rows):
    count = 0
    for row in rows:
        for element in row:
            if element == SAFE:
                count += 1
    return count


if __name__ == '__main__':
    main()
