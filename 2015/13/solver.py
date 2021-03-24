import math
import itertools
from collections import defaultdict

import aoc_search
from aoc_board import Grid, Point
from aoc_computer import Computer
from aoc_parser import Parser


TEST = False
FILE_NAME = 'sample' if TEST else 'data'


def main():
    # Part 1 = 709
    get_max_score(False)
    # Part 2 = 668
    get_max_score(True)


def get_max_score(include_self):
    graph = get_graph()
    scores = []
    for permutation in get_permutations(graph, include_self):
        score = get_score(permutation, graph)
        scores.append(score)
    print(max(scores))


def get_permutations(graph, include_self):
    keys = set(graph.keys())
    if include_self:
        keys.add('Vlad')
    return itertools.permutations(keys)


def get_score(permutation, graph):
    score = 0
    for i in range(len(permutation)):
        current = permutation[i]
        values = graph[current]

        left = permutation[(i - 1) % len(permutation)]
        right = permutation[(i + 1) % len(permutation)]
        
        score += values[left]
        score += values[right]
    return score


def get_graph():
    graph = defaultdict(lambda: defaultdict(int))
    for line in Parser(FILE_NAME).lines():
        line = line[:-1].split()

        who = line[0]

        multiplier = 1 if line[2] == 'gain' else -1
        amount = int(line[3])
        weight = multiplier * amount

        adjacent = line[10]

        graph[who][adjacent] = weight
    return graph


if __name__ == '__main__':
    main()

