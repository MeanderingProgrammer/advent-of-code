from collections import defaultdict

from commons.aoc_parser import Parser


class Room:

    def __init__(self, value):
        value = value.split('-')
        self.name = '-'.join(value[:-1])
        sector_id_checksum = value[-1].split('[')
        self.sector_id = int(sector_id_checksum[0])
        self.checksum = sector_id_checksum[1][:-1]

    def valid(self):
        frequencies = defaultdict(int)
        for ch in self.name:
            frequencies[ch] += 1

        expected_checksum = list(set([ch for ch in self.name if ch != '-']))
        expected_checksum.sort(key=lambda ch: (-frequencies[ch], ch))
        expected_checksum = expected_checksum[:len(self.checksum)]
        expected_checksum = ''.join(expected_checksum)

        return self.checksum == expected_checksum

    def decrypt(self):
        decrypted = []
        for ch in self.name:
            if ch == '-':
                decrypted.append(' ')
            else:
                away_from_a = ord(ch) - ord('a')
                away_from_a += self.sector_id
                away_from_a %= 26
                decrypted_id = ord('a') + away_from_a
                decrypted.append(chr(decrypted_id))
        return ''.join(decrypted)


def main():
    rooms = get_rooms()
    rooms = [room for room in rooms if room.valid()]
    sectors = [room.sector_id for room in rooms]
    # Part 1: 278221
    print('Part 1: {}'.format(sum(sectors)))

    store_room = 'northpole object storage'
    north_pole_room = [room for room in rooms if room.decrypt() == store_room][0]
    # Part 2: 267
    print('Part 2: {}'.format(north_pole_room.sector_id))


def get_rooms():
    return [Room(line) for line in Parser().lines()]


if __name__ == '__main__':
    main()
