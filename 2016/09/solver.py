from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Compressed:
    compressed: str

    def decompress(self, recursive: bool) -> int:
        result: int = 0
        i: int = 0
        while i < len(self.compressed):
            if self.compressed[i] == "(":
                end, length, times = self.get_repeat_details(i + 1)
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

    def get_repeat_details(self, start: int) -> tuple[int, int, int]:
        end = self.compressed.index(")", start)
        length, times = self.compressed[start:end].split("x")
        return end, int(length), int(times)


@answer.timer
def main() -> None:
    answer.part1(102239, decompress(False))
    answer.part2(10780403063, decompress(True))


def decompress(recursive: bool) -> int:
    return Compressed(Parser().string()).decompress(recursive)


if __name__ == "__main__":
    main()
