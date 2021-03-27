from program import Program

DEBUG = False


def main():
    # Part 1: 12234644
    print('Part 1: {}'.format(run_program(1)))
    # Part 2: 3508186
    print('Part 2: {}'.format(run_program(5)))


def run_program(system_id):
    program = Program(get_memory(), system_id, DEBUG)
    program.run()
    return program.diagnostic_code()


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
