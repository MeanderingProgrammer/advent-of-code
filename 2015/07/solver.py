from dataclasses import dataclass
from typing import Optional, Self

from aoc import answer
from aoc.parser import Parser


@dataclass
class Value:
    value: list[str]
    evaluated: Optional[int] = None

    def evaluate(self, diagram: dict[str, Self]) -> int:
        if self.evaluated is None:
            self.evaluated = self.compute(diagram)
        return self.evaluated

    def compute(self, diagram: dict[str, Self]) -> int:
        if len(self.value) == 1:
            return self.get_value(diagram, 0)
        elif len(self.value) == 2:
            return ~self.get_value(diagram, 1)
        elif len(self.value) == 3:
            v1 = self.get_value(diagram, 0)
            operator = self.value[1]
            if operator == "AND":
                return v1 & self.get_value(diagram, 2)
            elif operator == "OR":
                return v1 | self.get_value(diagram, 2)
            elif operator == "LSHIFT":
                return v1 << int(self.value[2])
            elif operator == "RSHIFT":
                return v1 >> int(self.value[2])
        raise Exception(f"No idea how to handle: {self.value}")

    def get_value(self, diagram: dict[str, Self], index: int):
        variable: str = self.value[index]
        if variable in diagram:
            return diagram[variable].evaluate(diagram)
        else:
            return int(variable)


def main() -> None:
    first = evaluate(None)
    answer.part1(3176, first)
    answer.part2(14710, evaluate(first))


def evaluate(b_override: Optional[int]) -> int:
    diagram: dict[str, Value] = get_diagram()
    if b_override is not None:
        diagram["b"] = Value(str(b_override).split())
    return diagram["a"].evaluate(diagram)


def get_diagram() -> dict[str, Value]:
    diagram: dict[str, Value] = dict()
    for line in Parser().lines():
        value, key = line.split(" -> ")
        diagram[key] = Value(value.split())
    return diagram


if __name__ == "__main__":
    main()
