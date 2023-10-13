from aoc import answer


START_STATE = "10001110011110000"
DESIRED_LENGTH = 272


class Curve:
    def __init__(self, value):
        self.value = value

    def modify(self):
        reverse_flipped = self.flip(self.value[::-1])
        self.value += "0" + reverse_flipped

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value

    @staticmethod
    def flip(value):
        result = []
        for v in value:
            add = "0" if v == "1" else "1"
            result.append(add)
        return "".join(result)


def main():
    answer.part1("10010101010011101", fill_disk(DESIRED_LENGTH))
    answer.part2("01100111101101111", fill_disk(35_651_584))


def fill_disk(length):
    curve = Curve(START_STATE)
    while len(curve) < length:
        curve.modify()
    return get_checksum(str(curve)[:length])


def get_checksum(value):
    result = []
    for i in range(len(value) // 2):
        start_index = i * 2
        first, second = value[start_index], value[start_index + 1]
        add = "1" if first == second else "0"
        result.append(add)
    result = "".join(result)
    return result if len(result) % 2 == 1 else get_checksum(result)


if __name__ == "__main__":
    main()
