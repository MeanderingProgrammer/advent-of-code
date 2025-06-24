from dataclasses import dataclass
from typing import Self

from aoc import answer
from aoc.parser import Parser

type Rules = dict[int, list[int]]


@dataclass(frozen=True)
class Order:
    pages: list[int]

    def middle(self) -> int:
        return self.pages[len(self.pages) // 2]

    def valid(self, rules: Rules) -> bool:
        seen: set[int] = set()
        for page in self.pages:
            seen.add(page)
            for illegal in rules.get(page, []):
                if illegal in seen:
                    return False
        return True

    def fix(self, deps: Rules) -> Self:
        pages: list[int] = []
        while len(self.pages) > 0:
            page = self.next(deps)
            assert page is not None
            pages.append(page)
        return type(self)(pages)

    def next(self, deps: Rules) -> int | None:
        for i, page in enumerate(self.pages):
            if not self.has(deps.get(page, [])):
                return self.pages.pop(i)
        return None

    def has(self, illegal: list[int]) -> bool:
        for page in illegal:
            if page in self.pages:
                return True
        return False


@answer.timer
def main() -> None:
    groups = Parser().line_groups()
    rules = parse_rules(groups[0], True)
    deps = parse_rules(groups[0], False)
    orders = parse_orders(groups[1])
    answer.part1(5248, sum_middle(rules, deps, orders, False))
    answer.part2(4507, sum_middle(rules, deps, orders, True))


def parse_rules(lines: list[str], forward: bool) -> Rules:
    rules: Rules = dict()
    for line in lines:
        v1, v2 = line.split("|")
        left, right = int(v1), int(v2)
        src = left if forward else right
        dst = right if forward else left
        if src not in rules:
            rules[src] = []
        rules[src].append(dst)
    return rules


def parse_orders(lines: list[str]) -> list[Order]:
    orders: list[Order] = []
    for line in lines:
        order = Order([int(value) for value in line.split(",")])
        orders.append(order)
    return orders


def sum_middle(rules: Rules, deps: Rules, orders: list[Order], fix: bool) -> int:
    result: int = 0
    for order in orders:
        valid = order.valid(rules)
        if valid and not fix:
            result += order.middle()
        if not valid and fix:
            result += order.fix(deps).middle()
    return result


if __name__ == "__main__":
    main()
