import hashlib
from aoc import answer
from aoc.parser import Parser


def main():
    door_id = Parser().string()
    answer.part1("d4cd2ee1", generate_password(door_id, populate_v1))
    answer.part2("f2c730e5", generate_password(door_id, populate_v2))


def generate_password(door_id, populator):
    password, i = [None] * 8, 0
    while not all(password):
        value = door_id + str(i)
        hashed = hash(value)
        if hashed[:5] == "00000":
            populator(password, hashed)
        i += 1
    return "".join(password)


def hash(value):
    return hashlib.md5(str.encode(value)).hexdigest()


def populate_v1(password, hashed):
    index = sum([ch is not None for ch in password])
    password[index] = hashed[5]


def populate_v2(password, hashed):
    index = hashed[5]
    valid_indexes = [str(i) for i in range(len(password))]
    if index in valid_indexes:
        index = int(index)
        if password[index] is None:
            password[index] = hashed[6]


if __name__ == "__main__":
    main()
