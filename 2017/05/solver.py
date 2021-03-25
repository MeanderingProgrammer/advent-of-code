from aoc_parser import Parser


FILE_NAME = 'data'


def main():
    # Part 1: 373160
    print('Part 1: {}'.format(run(increment_v1)))
    # Part 2: 26395586
    print('Part 2: {}'.format(run(increment_v2)))


def run(f):
    jumps = Parser(FILE_NAME).int_lines()
    steps, ip = 0, 0
    while ip >= 0 and ip < len(jumps):
        jump = jumps[ip]
        jumps[ip] = f(jump)
        ip += jump
        steps += 1
    return steps


def increment_v1(current):
    return current + 1


def increment_v2(current):
    if current >= 3:
        return current - 1
    else:
        return current + 1


if __name__ == '__main__':
    main()
