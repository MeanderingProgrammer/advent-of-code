import numpy as np
from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


class Value:

    def __init__(self, value):
        self.value = value.split()
        self.evaluated = None

    def evaluate(self, diagram):
        if self.evaluated is not None:
            return self.evaluated

        if len(self.value) == 1:
            result = self.get_value(self.value[0], diagram)
        elif len(self.value) == 2:
            result = ~self.get_value(self.value[1], diagram)
        elif len(self.value) == 3:
            v1 = self.get_value(self.value[0], diagram)
            operator = self.value[1]
            
            if operator in ['AND', 'OR']:
                v2 = self.get_value(self.value[2], diagram)
                if operator == 'AND':
                    result = v1 & v2
                elif operator == 'OR':
                    result = v1 | v2
            elif operator in ['LSHIFT', 'RSHIFT']:
                v2 = int(self.value[2])
                if operator == 'LSHIFT':
                    result = v1 << v2
                elif operator == 'RSHIFT':
                    result = v1 >> v2
            else:
                raise Exception('No idea how to handle: {}'.format(self.value))
        else:
            raise Exception('No idea how to handle: {}'.format(self.value))

        result = np.array([result], dtype='uint16')[0]
        self.evaluated = result
        return result

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ' '.join(self.value)

    @staticmethod
    def get_value(variable, diagram):
        if variable in diagram:
            return diagram[variable].evaluate(diagram)
        else:
            return int(variable)


def main():
    # Part 1 = 3176
    first = evaluate(None)
    print('First value for a: {}'.format(first))
    # Part 2 = 14710
    second = evaluate(first)
    print('Second value for a: {}'.format(second))


def evaluate(b_override):
    diagram = get_diagram()
    if b_override is not None:
        diagram['b'] = Value(str(b_override))
    return diagram['a'].evaluate(diagram)


def get_diagram():
    diagram = {}
    for line in Parser(FILE_NAME).lines():
        line = line.split(' -> ')
        diagram[line[1]] = Value(line[0])
    return diagram


if __name__ == '__main__':
    main()

