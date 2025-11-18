from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Room:
    name: str
    sector_id: int
    checksum: str

    @classmethod
    def new(cls, s: str) -> Self:
        name, sector_id_checksum = s.rsplit("-", 1)
        sector_id, checksum = sector_id_checksum.split("[")
        return cls(name, int(sector_id), checksum[:-1])

    def valid(self) -> bool:
        frequencies: dict[str, int] = defaultdict(int)
        for ch in self.name:
            frequencies[ch] += 1
        expected_checksum = list(set([ch for ch in self.name if ch != "-"]))
        expected_checksum.sort(key=lambda ch: (-frequencies[ch], ch))
        expected_checksum = expected_checksum[: len(self.checksum)]
        return self.checksum == "".join(expected_checksum)

    def decrypt(self) -> str:
        decrypted: list[str] = []
        for ch in self.name:
            if ch == "-":
                decrypted.append(" ")
            else:
                index = ((ord(ch) - ord("a")) + self.sector_id) % 26
                decrypted.append(chr(ord("a") + index))
        return "".join(decrypted)


@answer.timer
def main() -> None:
    rooms = [Room.new(line) for line in Parser().lines()]
    rooms = [room for room in rooms if room.valid()]
    answer.part1(278221, sum([room.sector_id for room in rooms]))
    north_pole_room = filter(
        lambda room: room.decrypt() == "northpole object storage", rooms
    )
    answer.part2(267, next(north_pole_room).sector_id)


if __name__ == "__main__":
    main()
