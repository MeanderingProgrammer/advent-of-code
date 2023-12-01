from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Number:
    value: int

    def evaluate(self, _: bool) -> int:
        return self.value


@dataclass(frozen=True)
class Expression:
    expressions: list[Self | Number]
    operators: list[str]

    def evaluate(self, addition: bool) -> int:
        if len(self.expressions) == 1:
            return self.expressions[0].evaluate(addition)
        if addition:
            operator = "+" if "+" in self.operators else "*"
            index = self.operators.index(operator)
        else:
            operator = self.operators[0]
            index = 0
        left = self.expressions[index].evaluate(addition)
        right = self.expressions[index + 1].evaluate(addition)
        result = left + right if operator == "+" else left * right
        self.expressions[index] = Number(result)
        del self.expressions[index + 1]
        del self.operators[index]
        return self.evaluate(addition)


def main() -> None:
    answer.part1(69490582260, sum_expressions(False))
    answer.part2(362464596624526, sum_expressions(True))


def sum_expressions(addition: bool) -> int:
    return sum([expression.evaluate(addition) for expression in get_expressions()])


def get_expressions() -> list[Expression]:
    def get_end_index(start: int, line: str) -> int:
        count = 0
        for i in range(start, len(line)):
            char = line[i]
            if char == "(":
                count += 1
            elif char == ")":
                count -= 1
                if count == 0:
                    return i
        raise Exception("Failed")

    def parse_expression(line: str) -> Expression:
        expressions: list[Expression | Number] = []
        operators: list[str] = []
        i = 0
        while i < len(line):
            char = line[i]
            if char == "(":
                end_index = get_end_index(i, line)
                expressions.append(parse_expression(line[i + 1 : end_index]))
                i = end_index + 1
            elif char.isdigit():
                expressions.append(Number(int(char)))
                i += 1
            else:
                operators.append(char)
                i += 1
        return Expression(expressions, operators)

    return [parse_expression(line.replace(" ", "")) for line in Parser().lines()]


if __name__ == "__main__":
    main()
