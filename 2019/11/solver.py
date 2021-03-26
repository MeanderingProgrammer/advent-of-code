from program import Program

DEBUG = False

import numpy as np
from PIL import Image


class Direction:

    def __init__(self):
        self.index = 0
        self.directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        ]

    def rotate(self, value):
        self.index += (value if value == 1 else -1)

    def step(self, position):
        to_go = self.directions[self.index % len(self.directions)]
        return position[0] + to_go[0], position[1] + to_go[1]

class PaintBot:

    def __init__(self, memory, starting_color):
        self.program = Program(get_memory(), self, DEBUG)
        self.color = True
        
        self.direction = Direction()
        self.grid = {}
        self.position = (0, 0)
        self.grid[self.position] = starting_color

    def run(self):
        while self.program.has_next():
            self.program.next()

    def get_input(self):
        return self.grid[self.position] if self.position in self.grid else 0

    def add_output(self, value):
        if self.color:
            self.grid[self.position] = value
        else:
            self.direction.rotate(value)
            self.position = self.direction.step(self.position)
        self.color = not self.color

    def save_grid(self):
        xs = [position[0] for position in self.grid]
        ys = [position[1] for position in self.grid]
        rows = []
        for y in range(min(ys), max(ys)+1):
            row = []
            for x in range(max(xs), min(xs) - 1, -1):
                row.append(self.grid.get((x, y), 0))
            rows.append(row)
        rows = 255 * np.array(rows).astype(np.uint8)
        Image.fromarray(rows, mode='L').save('part-2.png')


def main():
    #solve_part_1()
    solve_part_2()


def solve_part_1():
    # Part 1 = 1909
    bot = PaintBot(get_memory(), 0)
    bot.run()
    print('Total panels painted = {}'.format(len(bot.grid)))


def solve_part_2():
    # Part 2 = 
    bot = PaintBot(get_memory(), 1)
    bot.run()
    bot.save_grid()


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
