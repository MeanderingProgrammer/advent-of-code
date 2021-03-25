import hashlib 


SALT = 'iwrupvqb'


def main():
    # Part 1: 346386
    print('Part 1: {}'.format(first_index(5)))
    # Part 2: 9958218
    print('Part 2: {}'.format(first_index(6)))


def first_index(leading_zeros):
    goal = '0' * leading_zeros
    i = 1
    while True:
        value = SALT + str(i)
        hashed = hash(value)
        if hashed[:leading_zeros] == goal:
            return i
        i += 1


def hash(value):
    return hashlib.md5(str.encode(value)).hexdigest()


if __name__ == '__main__':
    main()
