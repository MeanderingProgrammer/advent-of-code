from aoc import answer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    board = Parser().lines()

    trees: list[int] = []
    for traversal in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        trees.append(traverse(board, traversal[0], traversal[1]))
    answer.part1(220, trees[1])

    result = 1
    for tree in trees:
        result *= tree
    answer.part2(2138320800, result)


def traverse(board: list[str], r_step: int, d_step: int) -> int:
    x_pos = 0
    num_trees = 0
    for i in range(0, len(board), d_step):
        row = board[i]
        length = len(row)
        value = row[x_pos % length]
        if value == "#":
            num_trees += 1
        x_pos += r_step
    return num_trees


if __name__ == "__main__":
    main()
