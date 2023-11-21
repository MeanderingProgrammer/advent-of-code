from aoc import answer
from aoc.parser import Parser


def main() -> None:
    answer.part1("10010101010011101", fill_disk(272))
    answer.part2("01100111101101111", fill_disk(35_651_584))


def fill_disk(length: int) -> str:
    curve: list[bool] = [value == "1" for value in Parser(strip=True).string()]
    while len(curve) < length:
        flipped = [not value for value in curve[::-1]]
        curve.append(False)
        curve.extend(flipped)
    checksum = get_checksum(curve[:length])
    return "".join(["1" if value else "0" for value in checksum])


def get_checksum(value: list[bool]) -> list[bool]:
    result: list[bool] = []
    for i in range(0, len(value), 2):
        result.append(value[i] == value[i + 1])
    return result if len(result) % 2 == 1 else get_checksum(result)


if __name__ == "__main__":
    main()
