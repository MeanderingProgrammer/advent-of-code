class Transformer:

    def __init__(self, subject):
        self.subject = subject

    def get_loop_size(self, goal):
        value = 1
        loop_size = 0
        while value != goal:
            loop_size += 1
            value = self.get_next_value(value)
        return loop_size

    def run_loop(self, loop_size):
        value = 1
        for i in range(loop_size):
            value = self.get_next_value(value)
        return value

    def get_next_value(self, value):
        value *= self.subject
        return value % 20201227


def main():
    card_pub, door_pub = get_keys()
    # Part 1: 3015200
    print_encryption_key(card_pub, door_pub, 'card')
    print_encryption_key(door_pub, card_pub, 'door')


def print_encryption_key(public_key, other_public_key, source):
    loop_size = Transformer(7).get_loop_size(public_key)
    encryption_key = Transformer(other_public_key).run_loop(loop_size)
    print('Result from {} = {}'.format(source, encryption_key))


def get_keys():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        keys = f.read().splitlines()
    return int(keys[0]), int(keys[1])


if __name__ == '__main__':
    main()
