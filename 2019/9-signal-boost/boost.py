from program import Program
from itertools import permutations

DEBUG = False


def main():
    solve_part_1()
    solve_part_2()


def solve_part_1():
    # Part 1 = 3512778005
    program = get_program(1)
    program.run()
    print(program.outputs)


def solve_part_2():
    # Part 2 = 35920
    program = get_program(2)
    program.run()
    print(program.outputs)


def get_program(param):
    return Program(get_memory(), param, DEBUG)


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
