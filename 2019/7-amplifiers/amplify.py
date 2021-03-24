from program import Program
from itertools import permutations

DEBUG = False


def main():
    solve_part_1()
    solve_part_2()


def solve_part_1():
    # Part 1 = 38834
    max_value = 0
    for sequence in permutations([0, 1, 2, 3, 4]):
        value = run_sequence(sequence)
        if value > max_value:
            max_value = value
    print('Maximum value = {}'.format(max_value))


def solve_part_2():
    # Part 2 = 69113332
    max_value = 0
    for sequence in permutations([5, 6, 7, 8, 9]):
        value = run_sequence_loop(sequence)
        if value > max_value:
            max_value = value
    print('Maximum value = {}'.format(max_value))


def run_sequence(sequence):
    output = 0
    amplifiers = get_amplifiers(sequence)
    for amplifier in amplifiers:
        amplifier.add_input(output)
        amplifier.run()
        output = amplifier.get_output()
    return output


def run_sequence_loop(sequence):
    output = 0
    state = None
    amplifiers = get_amplifiers(sequence)

    while state is None or state.output:
        for amplifier in amplifiers:
            amplifier.add_input(output)
            state = amplifier.run_output()
            if state.halt:
                break
            output = amplifier.get_output()

    return amplifiers[-1].get_output()


def get_amplifiers(sequence):
    return [Program(get_memory(), entry, DEBUG) for entry in sequence]


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
