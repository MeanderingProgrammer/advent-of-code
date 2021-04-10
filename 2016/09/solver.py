from commons.aoc_parser import Parser


class Compressed:

    def __init__(self, compressed, recursive):
        self.compressed = compressed
        self.recursive = recursive

    def decompress(self):
        result, i = [], 0
        while i < len(self.compressed):
            ch = self.compressed[i]
            if ch == '(':
                end, (length, times) = self.get_repeat_details(i+1)
                i = end + 1
                section = self.compressed[i:i+length]
                if self.recursive:
                    section = Compressed(section, self.recursive).decompress()
                result.append(section * times)
                i += length
            else:
                result.append(ch)
                i += 1
        return ''.join(result)

    def get_repeat_details(self, start):
        end = self.compressed.index(')', start)
        return end, self.parse_details(self.compressed[start:end])

    @staticmethod
    def parse_details(details):
        details = details.split('x')
        return int(details[0]), int(details[1])


def main():
    # Part 1: 102239
    print('Part 1: {}'.format(decompress(False)))
    # Part 2: 10780403063
    print('Part 2: {}'.format(decompress(True)))


def decompress(recursive):
    compressed = Compressed(Parser().string(), recursive)
    return len(compressed.decompress())


if __name__ == '__main__':
    main()
