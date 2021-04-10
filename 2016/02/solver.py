from commons.aoc_parser import Parser
from commons.aoc_board import Grid, Point


CONTROLS = {
    'U': Point(0, -1),
    'D': Point(0, 1),
    'L': Point(-1, 0),
    'R': Point(1, 0)
}


def main():
    # Part 1: 47978
    print('Part 1: {}'.format(get_code(*create_phone(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    ))))
    # Part 2: 659AD
    print('Part 2: {}'.format(get_code(*create_phone(
        [
            ['*', '*',  1 , '*', '*'],
            ['*',  2 ,  3 ,  4 , '*'],
            [ 5 ,  6 ,  7 ,  8 ,  9 ],
            ['*', 'A', 'B', 'C', '*'],
            ['*', '*', 'D', '*', '*']
        ]
    ))))


def get_code(phone, position):
    code = ''
    for instruction in get_instructions():
        position = follow(phone, position, instruction)
        code += str(phone[position])
    return code


def follow(phone, position, instruction):
    for direction in instruction:
        new_position = position + CONTROLS[direction]
        if new_position in phone:
            position = new_position
    return position


def create_phone(pattern):
    phone, start = Grid(), None
    for y, row in enumerate(pattern):
        for x, value in enumerate(row):
            point = Point(x, y)
            if value != '*':
                phone[point] = value
            if value == 5:
                start = point
    return phone, start


def get_instructions():
    return Parser().lines()


if __name__ == '__main__':
    main()
