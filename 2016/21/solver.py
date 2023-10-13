from aoc import answer
from aoc.parser import Parser


class Scrambler:
    def __init__(self, value):
        self.value = [v for v in value]

    def scramble(self, raw_rule):
        rule = raw_rule.split()
        if rule[0] == "swap":
            if rule[1] == "position":
                index_1, index_2 = int(rule[2]), int(rule[5])
            elif rule[1] == "letter":
                index_1, index_2 = self.value.index(rule[2]), self.value.index(rule[5])
            else:
                raise Exception("Unknown Swap Rule: {}".format(rule))
            temp = self.value[index_1]
            self.value[index_1] = self.value[index_2]
            self.value[index_2] = temp
        elif rule[0] == "rotate":
            if rule[1] == "left":
                amount_right = len(self.value) - int(rule[2])
            elif rule[1] == "right":
                amount_right = int(rule[2])
            elif rule[1] == "based":
                index = self.value.index(rule[6])
                amount_right = 1 + index
                if index >= 4:
                    amount_right += 1
            else:
                raise Exception("Unknown Rotate Rule: {}".format(rule))
            self.rotate_right(amount_right)
        elif rule[0] == "reverse":
            start, end = int(rule[2]), int(rule[4])
            substring = self.value[start : end + 1]
            substring.reverse()
            for i in range(len(substring)):
                self.value[start + i] = substring[i]
        elif rule[0] == "move":
            start, end = int(rule[2]), int(rule[5])
            at_start = self.value[start]
            del self.value[start]
            self.value.insert(end, at_start)
        else:
            raise Exception("Unknown Rule: {}".format(rule))

    def unscramble(self, raw_rule):
        rule = raw_rule.split()
        if rule[0] == "swap":
            if rule[1] == "position":
                index_1, index_2 = int(rule[2]), int(rule[5])
            elif rule[1] == "letter":
                index_1, index_2 = self.value.index(rule[2]), self.value.index(rule[5])
            else:
                raise Exception("Unknown Swap Rule: {}".format(rule))
            temp = self.value[index_1]
            self.value[index_1] = self.value[index_2]
            self.value[index_2] = temp
        elif rule[0] == "rotate":
            if rule[1] == "left":
                self.rotate_right(int(rule[2]))
            elif rule[1] == "right":
                self.rotate_right(len(self.value) - int(rule[2]))
            elif rule[1] == "based":
                goal = str(self)
                for i in range(len(self.value)):
                    self.rotate_right(-1)
                    scrambler = Scrambler(self.value)
                    scrambler.scramble(raw_rule)
                    end = str(scrambler)
                    if goal == end:
                        break
            else:
                raise Exception("Unknown Rotate Rule: {}".format(rule))
        elif rule[0] == "reverse":
            start, end = int(rule[2]), int(rule[4])
            substring = self.value[start : end + 1]
            substring.reverse()
            for i in range(len(substring)):
                self.value[start + i] = substring[i]
        elif rule[0] == "move":
            start, end = int(rule[5]), int(rule[2])
            at_start = self.value[start]
            del self.value[start]
            self.value.insert(end, at_start)
        else:
            raise Exception("Unknown Rule: {}".format(rule))

    def rotate_right(self, amount):
        amount %= len(self.value)
        from_end = self.value[-amount:]
        self.value = self.value[:-amount]
        self.value = from_end + self.value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "".join(self.value)


def main():
    answer.part1("bdfhgeca", scramble("abcdefgh"))
    answer.part2("gdfcabeh", unscramble("fbgdceah"))


def scramble(value):
    scrambler = Scrambler(value)
    for line in get_lines():
        scrambler.scramble(line)
    return str(scrambler)


def unscramble(value):
    scrambler = Scrambler(value)
    lines = get_lines()
    lines.reverse()
    for line in lines:
        scrambler.unscramble(line)
    return str(scrambler)


def get_lines():
    return Parser().lines()


if __name__ == "__main__":
    main()
