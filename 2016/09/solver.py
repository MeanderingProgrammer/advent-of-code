from aoc import answer
from aoc.parser import Parser


class Compressed:
    def __init__(self, compressed):
        self.compressed = compressed

    def decompress(self, recursive):
        result, i = 0, 0
        while i < len(self.compressed):
            if self.compressed[i] == "(":
                end, (length, times) = self.get_repeat_details(i + 1)
                i = end + 1
                if recursive:
                    section = self.compressed[i : i + length]
                    section_length = Compressed(section).decompress(recursive)
                else:
                    section_length = length
                result += section_length * times
                i += length
            else:
                result += 1
                i += 1
        return result

    def get_repeat_details(self, start):
        end = self.compressed.index(")", start)
        return end, self.parse_details(self.compressed[start:end])

    @staticmethod
    def parse_details(details):
        details = details.split("x")
        return int(details[0]), int(details[1])


def main():
    answer.part1(102239, decompress(False))
    answer.part2(10780403063, decompress(True))


def decompress(recursive):
    compressed = Compressed(Parser().string())
    return compressed.decompress(recursive)


if __name__ == "__main__":
    main()
