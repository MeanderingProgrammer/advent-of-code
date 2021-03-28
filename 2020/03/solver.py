def main():
    board = get_board()
    traversals = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]

    trees = []
    for traversal in traversals:
        trees.append(traverse(board, traversal[0], traversal[1]))

    # Part 1: 220
    print('Part 1: {}'.format(trees[1]))
    result = 1
    for tree in trees:
        result *= tree
    # Part 2: 2138320800
    print('Part 2: {}'.format(result))


def traverse(board, r_step, d_step):
    x_pos = 0
    num_trees = 0

    for i in range(0, len(board), d_step):
        row = board[i]
        length = len(row)
        value = row[x_pos % length]
        if value == '#':
            num_trees += 1
        x_pos += r_step

    return num_trees


def get_board():
    board = []
    f = open('data.txt', 'r')

    for line in f:
        board.append(line.strip())

    f.close()
    return board


if __name__ == '__main__':
    main()
