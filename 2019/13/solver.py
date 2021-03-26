from program import Program

DEBUG = False

TILE_MAPPING = {
    0: 'empty',
    1: 'wall',
    2: 'block',
    3: 'horizontal paddle',
    4: 'ball'
}

class Tile:

    def __init__(self, x_pos, y_pos, tile):
        self.x_pos, self.y_pos, self.tile = x_pos, y_pos, tile
        self.tile_name = TILE_MAPPING[tile]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} at ({}, {})'.format(self.tile_name, self.x_pos, self.y_pos)

class Game:

    def __init__(self, memory):
        self.program = Program(memory, self, DEBUG)
        self.score = 0
        self.tiles = []
        self.tile_buffer = []

    def play(self):
        while self.program.has_next():
            self.program.next()

    def get_input(self):
        ball_x = self.get_tiles('ball')[-1].x_pos
        paddle_x = self.get_tiles('horizontal paddle')[-1].x_pos
        pos_diff = ball_x - paddle_x
        if pos_diff < 0:
            return -1
        elif pos_diff > 0:
            return 1
        else:
            return 0

    def add_output(self, value):
        self.tile_buffer.append(value)
        if len(self.tile_buffer) == 3:
            x, y, value = self.tile_buffer
            if x == -1 and y == 0:
                self.score = value
            else:
                self.tiles.append(Tile(x, y, value))
            self.tile_buffer = []

    def get_tiles(self, tile_name):
        return [tile for tile in self.tiles if tile.tile_name == tile_name]

def main():
    #solve_part_1()
    solve_part_2()


def solve_part_1():
    # Part 1 = 363
    game = Game(get_memory())
    game.play()
    print('Total block tiles = {}'.format(len(game.get_tiles('block'))))


def solve_part_2():
    # Part 2 = 17159
    memory = get_memory()
    # Override address 0 to 2 to play for free
    memory[0] = 2
    game = Game(memory)
    game.play()
    print('Final score = {}'.format(game.score))


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
