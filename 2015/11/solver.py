from aoc import answer
from aoc.parser import Parser


class PasswordIncrementer:
    def __init__(self, starting_value):
        self.value = self.array(starting_value, self.to_index)

    def next(self):
        index = self.get_last_index_under(25)

        if index is not None:
            self.value[index] += 1
        else:
            self.value = [0] + self.value
            index = 0

        for i in range(index + 1, len(self.value)):
            self.value[i] = 0

    def valid(self):
        if not self.contains_triple():
            return False
        if self.contains_invalid():
            return False
        if not self.contains_pairs():
            return False
        return True

    def contains_triple(self):
        for i in range(len(self.value) - 2):
            first, second, third = self.value[i], self.value[i + 1], self.value[i + 2]
            if first + 1 == second and second + 1 == third:
                return True
        return False

    def contains_invalid(self):
        all_invalid = [self.to_index("i"), self.to_index("o"), self.to_index("l")]
        for invalid in all_invalid:
            if invalid in self.value:
                return True
        return False

    def contains_pairs(self):
        pairs = set()
        for i, character in enumerate(self.value[:-1]):
            if character == self.value[i + 1]:
                pairs.add(character)
        return len(pairs) > 1

    def get_value(self):
        characters = self.array(self.value, self.to_char)
        return "".join(characters)

    def get_last_index_under(self, n):
        for i in range(len(self.value) - 1, -1, -1):
            if self.value[i] < n:
                return i
        return None

    def array(self, values, transformer):
        return [transformer(value) for value in values]

    @staticmethod
    def to_index(character):
        return ord(character) - ord("a")

    @staticmethod
    def to_char(index):
        return chr(index + ord("a"))


def main():
    value = Parser(strip=True).string()
    generator = PasswordIncrementer(value)
    answer.part1("hxbxxyzz", run(generator))
    answer.part2("hxcaabcc", run(generator))


def run(generator):
    generator.next()
    while not generator.valid():
        generator.next()
    return generator.get_value()


if __name__ == "__main__":
    main()
