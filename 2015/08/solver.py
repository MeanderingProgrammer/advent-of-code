from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class String:
    value: str

    def total(self) -> int:
        return len(self.value)

    def decode(self) -> int:
        result: list[str] = []
        i: int = 0
        while i < len(self.value):
            ch = self.value[i]
            i += 1
            if ch == '"':
                continue
            result.append(ch)
            if ch == "\\":
                i += 3 if self.value[i] == "x" else 1
        return len(result)

    def encode(self) -> int:
        result: list[str] = ['"']
        for ch in self.value:
            if ch in ["\\", '"']:
                result.append("\\")
            result.append(ch)
        result.append('"')
        return len(result)


@answer.timer
def main() -> None:
    strings: list[String] = [String(line) for line in Parser().lines()]
    total = sum([s.total() for s in strings])
    answer.part1(1350, total - sum([s.decode() for s in strings]))
    answer.part2(2085, sum([s.encode() for s in strings]) - total)


if __name__ == "__main__":
    main()
