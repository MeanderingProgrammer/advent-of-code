from aoc_parser import Parser
from aoc_board import Grid, Point


class Elve:

    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.index)


class Recipes:

    def __init__(self):
        self.score_board = ['3', '7']
        self.elves = [
            Elve(0),
            Elve(1)
        ]

    def evolve(self, goal):
        while goal not in ''.join(self.score_board[-200_020:]):
            for i in range(100_000):
                combined = self.combine()
                self.add(combined)
                for elve in self.elves:
                    elve.index = (elve.index + self.score(elve.index) + 1) % len(self.score_board)

    def combine(self):
        return sum([self.score(elve.index) for elve in self.elves])

    def add(self, value):
        for i in str(value):
            self.score_board.append(i)

    def score(self, index):
        return int(self.score_board[index])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ''.join(self.score_board)


def main():
    # Input: 170_641
    goal = str(170_641)
    recipes = Recipes()
    recipes.evolve(goal)
    # Part 1: 2103141159
    print(''.join(recipes.score_board[int(goal):int(goal)+10]))
    # Part 2: 20165733
    print(str(recipes).index(goal))


if __name__ == '__main__':
    main()

