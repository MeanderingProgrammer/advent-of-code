import commons.answer as answer
from commons.aoc_parser import Parser


class String:

    def __init__(self, value):
        self.value = value

    def total(self):
        return len(self.value)

    def decode(self):
        result, i = [], 0
        while i < len(self.value):
            ch = self.value[i]
            if ch != '"':
                result.append(ch)
                if ch == '\\':
                    if self.value[i + 1] == 'x':
                        i += 3
                    else:
                        i += 1
            i += 1
        return len(result)

    def encode(self):
        result = ['"']
        for ch in self.value:
            if ch in ['\\', '"']:
                result.append('\\')
            result.append(ch)
        result.append('"')
        return len(result)


def main():
    total, decoded, encoded = 0, 0, 0

    for line in Parser().lines():
        s = String(line)

        total += s.total()
        decoded += s.decode()
        encoded += s.encode()

    answer.part1(1350, total - decoded)
    answer.part2(2085, encoded - total)


if __name__ == '__main__':
    main()
