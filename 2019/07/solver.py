from itertools import permutations

from program import Program


DEBUG = False


def main():
    # Part 1: 38834
    print('Part 1: {}'.format(run_permutations([0, 1, 2, 3, 4], False)))
    # Part 2: 69113332
    print('Part 2: {}'.format(run_permutations([5, 6, 7, 8, 9], True)))


def run_permutations(sequence, pause_on_load):
    values = []
    for sequence in permutations(sequence):
        value = run_sequence(sequence, pause_on_load)
        values.append(value)
    return max(values)


def run_sequence(sequence, pause_on_load):
    output, state, amplifiers = 0, True, get_amplifiers(sequence)

    while state:
        for amplifier in amplifiers:
            amplifier.add_input(output)
            state &= amplifier.run(pause_on_load)
            output = amplifier.get_output()

    return output


def get_amplifiers(sequence):
    return [Program(get_memory(), entry, DEBUG) for entry in sequence]


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
