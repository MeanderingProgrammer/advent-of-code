class PuzzleBoard:

    def __init__(self):
        self.board = {}

    def add(self, tile):
        if len(self.board) == 0:
            self.board[(0, 0)] = tile
            return True

        all_available = self.get_all_available()
        for available in all_available:
            edges_needed = self.get_edges_needed(available)
            for permutation in tile.permutations:
                if self.matches(permutation, edges_needed):
                    self.board[available] = permutation
                    return True
        return False

    def get_all_available(self):
        available = set()
        for position in self.board:
            available.update(self.get_adjacent(position))
        return available

    def get_edges_needed(self, position):
        edges_needed = []
        for i, adjacent in enumerate(self.get_adjacent(position)):
            opposing_edge = (i + 2) % 4
            if adjacent in self.board:
                edges_needed.append(self.board[adjacent].edges[opposing_edge])
            else:
                edges_needed.append(None)
        return edges_needed

    def coalesce(self):
        xs = []
        ys = []
        for position in self.board:
            xs.append(position[0])
            ys.append(position[1])

        rows = []
        for y in range(max(ys), min(ys)-1, -1):
            row = self.board[(min(xs), y)].remove_boarder()
            for x in range(min(xs)+1, max(xs)+1):
                row = row.add_horizontal(self.board[(x, y)].remove_boarder())
            rows.append(row)

        combined = rows[0]
        for i in range(1, len(rows)):
            combined = combined.add_vertical(rows[i])

        return combined

    def __str__(self):
        result = ''
        for position in self.board:
            result += '{}: {} \n'.format(position, self.board[position].identifier)
        return result

    @staticmethod
    def get_adjacent(position):
        return [
            (position[0]-1, position[1]),   # LEFT
            (position[0], position[1]+1),   # TOP
            (position[0]+1, position[1]),   # RIGHT
            (position[0], position[1]-1)    # BOTTOM
        ]

    @staticmethod
    def matches(tile, edges_needed):
        for i, edge in enumerate(tile.edges):
            needed = edges_needed[i]
            if needed is not None:
                if needed != edge:
                    return False
        return True


class ImageTile:

    def __init__(self, data, identifier=None):
        if identifier is None:
            self.identifier = int(data[0][5:-1])
            self.data = data[1:]
        else:
            self.identifier = identifier
            self.data = data
        size = len(self.data)
        self.edges = [
            ''.join(row[0] for row in self.data),       # LEFT
            self.data[0],                               # TOP
            ''.join(row[size-1] for row in self.data),  # RIGHT
            self.data[size-1]                           # BOTTOM
        ]

    def remove_boarder(self):
        boarderless = []
        for row in self.data[1:-1]:
            boarderless.append(row[1:-1])
        return ImageTile(boarderless, self.identifier)

    def add_horizontal(self, other):
        new_id = '{} + {}'.format(self.identifier, other.identifier)
        combined = []
        for i, row in enumerate(self.data):
            combined.append(row + other.data[i])
        return ImageTile(combined, new_id)

    def add_vertical(self, other):
        new_id = '{}\n{}'.format(self.identifier, other.identifier)
        combined = [row for row in self.data]
        combined.extend(other.data)
        return ImageTile(combined, new_id)

    def all_permutations(self):
        self.permutations = []
        tile = self
        for i in range(4):
            tile = tile.rotate()
            self.permutations.append(tile)
        tile = self.flip()
        for i in range(4):
            tile = tile.rotate()
            self.permutations.append(tile)

    def rotate(self):
        size = len(self.data)
        rotated = [[j for j in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                value = self.data[i][j]
                new_i = size - 1 - j
                new_j = i
                rotated[new_i][new_j] = value
        rotated = [''.join(row) for row in rotated]
        return ImageTile(rotated, self.identifier)


    def flip(self):
        size = len(self.data)
        rotated = [[j for j in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                value = self.data[i][j]
                new_j = size - 1 - j
                rotated[i][new_j] = value
        rotated = [''.join(row) for row in rotated]
        return ImageTile(rotated, self.identifier)

    def get_num_positive(self):
        num_positive = 0
        for row in self.data:
            for value in row:
                if value == '#':
                    num_positive += 1
        return num_positive

    def dimensions(self):
        length = len(self.data)
        width = len(self.data[0])
        return (width, length)

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = '{} \n'.format(self.identifier)
        return result + '\n'.join(self.data)


class SearchImage:

    def __init__(self, image):
        length = len(image)
        width = len(image[0])
        self.dimensions = (width, length)
        self.points = self.get_positive_points(image)

    def find_num_matches(self, tile):
        num_matches = 0
        for starting_point in self.starting_points(tile.dimensions()):
            cropped = self.crop(starting_point, tile)
            if self.does_match(cropped):
                num_matches += 1
        return num_matches

    def starting_points(self, dimensions):
        max_x = dimensions[0] - self.dimensions[0]
        max_y = dimensions[1] - self.dimensions[1]

        starting_points = []
        for x in range(max_x):
            for y in range(max_y):
                starting_points.append((x, y))
        return starting_points

    def crop(self, point, tile):
        cropped = []
        for i in range(self.dimensions[1]):
            row = tile.data[i+point[1]]
            cropped.append(row[point[0]:point[0]+self.dimensions[0]])
        return cropped

    def does_match(self, image):
        for point in self.points:
            value = image[point[1]][point[0]]
            if value != '#':
                return False
        return True

    @staticmethod
    def get_positive_points(image):
        positive_points = []
        for row in range(len(image)):
            for col in range(len(image[row])):
                value = image[row][col]
                if value == '#':
                    positive_points.append((col, row))
        return positive_points

def main():
    board = PuzzleBoard()
    solve_board(board)

    #solve_part_1(board)
    solve_part_2(board)


def solve_board(board):
    image_tiles = get_image_tiles()
    [image_tile.all_permutations() for image_tile in image_tiles]

    remaining_tiles = image_tiles
    while len(remaining_tiles) != 0:
        still_remaining = []
        for tile in remaining_tiles:
            if not board.add(tile):
                still_remaining.append(tile)

        # Luckily they didn't give input that caused us to need to 
        # implement recursive backtracking, yay!
        if len(remaining_tiles) == len(still_remaining):
            # Nothing was added should break with exception
            print(board.board)
            raise Exception('Was unable to add anything, something broken')

        remaining_tiles = still_remaining


def solve_part_1(board):
    # Part 1: 15003787688423
    xs = []
    ys = []
    for position in board.board:
        xs.append(position[0])
        ys.append(position[1])
    corners = [
        board.board[(min(xs), min(ys))].identifier,
        board.board[(min(xs), max(ys))].identifier,
        board.board[(max(xs), min(ys))].identifier,
        board.board[(max(xs), max(ys))].identifier
    ]
    value = 1
    for corner in corners:
        value *= corner
    print('Multiplied corners = {}'.format(value))


def solve_part_2(board):
    # Part 2: 1705
    image = board.coalesce()
    image_positive = image.get_num_positive()

    search_image = get_image_search()
    search_positive = len(search_image.points)

    image.all_permutations()
    for permutation in image.permutations:
        num_matches = search_image.find_num_matches(permutation)
        if num_matches > 0:
            roughness = image_positive - (num_matches * search_positive)
            print('Water roughness = {}'.format(roughness))


def get_image_tiles():
    filename = 'data'
    with open('{}.txt'.format(filename), 'r') as f:
        data = f.read().splitlines()

    splits = [i for i in range(len(data)) if data[i] == '']
    image_tiles = []

    previous = 0
    for split in splits:
        image_tiles.append(ImageTile(data[previous:split]))
        previous = split + 1
    image_tiles.append(ImageTile(data[previous:]))

    return image_tiles


def get_image_search():
    with open('sea-monster.txt', 'r') as f:
        data = f.read().splitlines()
    return SearchImage(data)


if __name__ == '__main__':
    main()
