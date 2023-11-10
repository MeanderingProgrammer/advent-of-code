from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass
class Curve:
    value: str

    def modify(self):
        reverse_flipped = self.flip(self.value[::-1])
        self.value += "0" + reverse_flipped

    @staticmethod
    def flip(value):
        result = []
        for v in value:
            add = "0" if v == "1" else "1"
            result.append(add)
        return "".join(result)


def main() -> None:
    curve = Curve(Parser(strip=True).string())
    answer.part1("10010101010011101", fill_disk(curve, 272))
    answer.part2("01100111101101111", fill_disk(curve, 35_651_584))


def fill_disk(curve: Curve, length: int) -> str:
    while len(curve.value) < length:
        curve.modify()
    return get_checksum(curve.value[:length])


def get_checksum(value: str) -> str:
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
