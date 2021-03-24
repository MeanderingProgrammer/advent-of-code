import hashlib 

import aoc_search
from aoc_parser import Parser
from aoc_board import Grid, Point


TEST = False
DOOR_ID = 'abc' if TEST else 'ugkcyxxp'


def main():
    # Part 1 = d4cd2ee1
    generate_password(populate_v1)
    # Part 2 = f2c730e5
    generate_password(populate_v2)


def generate_password(populator):
    password, i = [None]*8, 0
    while not all(password):
        value = DOOR_ID + str(i)
        hashed = hash(value)
        if hashed[:5] == '00000':
            populator(password, hashed)
        i += 1
    print('Password = {}'.format(''.join(password)))


def hash(value):
    return hashlib.md5(str.encode(value)).hexdigest()


def populate_v1(password, hashed):
    index = sum([ch is not None for ch in password])
    value = hashed[5]
    password[index] = value


def populate_v2(password, hashed):
    index = hashed[5]
    valid_indexes = [str(i) for i in range(len(password))]
    if index in valid_indexes:
        index = int(index)
        if password[index] is None:
            value = hashed[6]
            password[index] = value


if __name__ == '__main__':
    main()

