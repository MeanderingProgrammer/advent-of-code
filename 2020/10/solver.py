from collections import defaultdict
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Adapters:
    data: list[int]

    def chains(self) -> dict[int, int]:
        chains: dict[int, int] = defaultdict(int)
        for i in range(1, len(self.data)):
            chains[self.data[i] - self.data[i - 1]] += 1
        return chains

    def num_combinations(self) -> int:
        num_paths: list[int] = list(map(self.num_paths, self.data[:-1]))
        for i in range(len(num_paths) - 2, -1, -1):
            num_paths[i] = sum(num_paths[i + 1 : i + 1 + num_paths[i]])
        return num_paths[0]

    def num_paths(self, current: int) -> int:
        return sum(
            [adapter > current and adapter <= current + 3 for adapter in self.data]
        )


@answer.timer
def main() -> None:
    adapters = get_adapters()
    chains = adapters.chains()
    answer.part1(2343, chains[1] * chains[3])
    answer.part2(31581162962944, adapters.num_combinations())


def get_adapters() -> Adapters:
    data = sorted(Parser().int_lines())
    # Add starting & ending points
    data = [0] + data + [data[-1] + 3]
    return Adapters(data=data)


if __name__ == "__main__":
    main()
