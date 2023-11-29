from collections import defaultdict
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Entity:
    to: str
    value: int

    def process(
        self, value: int, bots: dict[int, "Bot"], outputs: dict[int, list[int]]
    ) -> None:
        if self.to == "bot":
            bots[self.value].process(value, bots, outputs)
        elif self.to == "output":
            outputs[self.value].append(value)
        else:
            raise Exception(f"Unknown type: {self.to}")


@dataclass(frozen=True)
class Bot:
    id: int
    low: Entity
    high: Entity
    values: list[int]
    held: list[int]

    def process(
        self, value: int, bots: dict[int, "Bot"], outputs: dict[int, list[int]]
    ) -> None:
        self.values.append(value)
        self.held.append(value)
        if len(self.values) == 2:
            self.low.process(min(self.values), bots, outputs)
            self.high.process(max(self.values), bots, outputs)
            self.values.clear()

    def held_all_values(self, values: list[int]) -> bool:
        for value in values:
            if value not in self.held:
                return False
        return True


def main() -> None:
    initial_values, bots = get_data()
    outputs = defaultdict(list)
    for bot, values in initial_values.items():
        for value in values:
            bots[bot].process(value, bots, outputs)
    answer.part1(118, get_bot(list(bots.values()), [17, 61]).id)
    answer.part2(143153, multiply_outputs(outputs, [0, 1, 2]))


def get_data() -> tuple[dict[int, list[int]], dict[int, Bot]]:
    initial_values: dict[int, list[int]] = defaultdict(list)
    bots = dict()
    for line in Parser().lines():
        parts = line.split()
        if parts[0] == "value":
            initial_values[int(parts[5])].append(int(parts[1]))
        if parts[0] == "bot":
            bots[int(parts[1])] = Bot(
                id=int(parts[1]),
                low=Entity(to=parts[5], value=int(parts[6])),
                high=Entity(to=parts[10], value=int(parts[11])),
                values=[],
                held=[],
            )
    return initial_values, bots


def get_bot(bots: list[Bot], values: list[int]) -> Bot:
    for bot in bots:
        if bot.held_all_values(values):
            return bot
    raise Exception("Failed")


def multiply_outputs(outputs: dict[int, list[int]], buckets: list[int]) -> int:
    result = 1
    for bucket in buckets:
        result *= outputs[bucket][0]
    return result


if __name__ == "__main__":
    main()
