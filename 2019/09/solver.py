from program import Program


DEBUG = False


def main():
    # Part 1: 3512778005
    print('Part 1: {}'.format(run(1)))
    # Part 2: 35920
    print('Part 2: {}'.format(run(2)))


def run(setting):
    program = get_program(setting)
    program.run()
    return program.outputs[0]


def get_program(param):
    return Program(get_memory(), param, DEBUG)


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
