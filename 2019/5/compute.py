from program import Program

DEBUG = False


def main():
    solve_part_1()
    solve_part_2()


def solve_part_1():
    # Part 1 = 12234644
    run_program(1)


def solve_part_2():
    # Part 2 = 3508186
    run_program(5)


def run_program(system_id):
    program = Program(get_memory(), system_id, DEBUG)
    program.run()
    print('Diagnostice code = {}'.format(program.diagnostic_code()))


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
