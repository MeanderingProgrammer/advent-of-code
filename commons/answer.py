def part1(expected, result):
    part(1, expected, result)


def part2(expected, result):
    part(2, expected, result)


def part(part, expected, result):
    if expected != result:
        raise Exception('Part {} incorrect, expected {} but got {}'.format(part, expected, result))
    print('Part {}: {}'.format(part, result))
