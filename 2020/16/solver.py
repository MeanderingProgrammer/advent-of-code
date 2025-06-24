from dataclasses import dataclass
from functools import reduce

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class ValueRange:
    start: int
    end: int

    def contains(self, value: int) -> bool:
        return value >= self.start and value <= self.end


@dataclass
class Rule:
    field_name: str
    value_ranges: list[ValueRange]
    row: int | None

    def matches(self, value: int) -> bool:
        return any([value_range.contains(value) for value_range in self.value_ranges])

    def starts_with(self, prefix: str) -> bool:
        return self.field_name.startswith(prefix)


@dataclass(frozen=True)
class Ticket:
    values: list[int]

    def unmatched_values(self, rules: list[Rule]) -> list[int]:
        return [
            value for value in self.values if not Ticket.matches_any_rule(value, rules)
        ]

    @staticmethod
    def matches_any_rule(value: int, rules: list[Rule]) -> bool:
        return any([rule.matches(value) for rule in rules])


@answer.timer
def main() -> None:
    groups = Parser().line_groups()
    rules = list(map(parse_rule, groups[0]))
    my_ticket = parse_ticket(groups[1][1])
    nearby_tickets = list(map(parse_ticket, groups[2][1:]))
    answer.part1(26980, solve_part_1(rules, nearby_tickets))
    answer.part2(3021381607403, solve_part_2(rules, my_ticket, nearby_tickets))


def parse_rule(line: str) -> Rule:
    def parse_value_range(raw: str) -> ValueRange:
        start, end = raw.split("-")
        return ValueRange(start=int(start), end=int(end))

    parts = line.split(": ")
    return Rule(
        field_name=parts[0],
        value_ranges=list(map(parse_value_range, parts[1].split(" or "))),
        row=None,
    )


def parse_ticket(line: str) -> Ticket:
    return Ticket(values=list(map(int, line.split(","))))


def solve_part_1(rules: list[Rule], nearby_tickets: list[Ticket]) -> int:
    unmatched_values: list[int] = []
    for ticket in nearby_tickets:
        unmatched_values.extend(ticket.unmatched_values(rules))
    return sum(unmatched_values)


def solve_part_2(
    rules: list[Rule], my_ticket: Ticket, nearby_tickets: list[Ticket]
) -> int:
    remaining_tickets: list[Ticket] = []
    for ticket in nearby_tickets:
        if len(ticket.unmatched_values(rules)) == 0:
            remaining_tickets.append(ticket)

    assign_rules(rules, remaining_tickets)
    departure_indexes = [rule.row for rule in rules if rule.starts_with("departure")]
    departure_values = [my_ticket.values[i] for i in departure_indexes if i is not None]
    return reduce((lambda x, y: x * y), departure_values)


def assign_rules(rules: list[Rule], tickets: list[Ticket]) -> None:
    while not all([rule.row is not None for rule in rules]):
        for i in range(len(rules)):
            values = [ticket.values[i] for ticket in tickets]
            possible_rules = get_possible_rules(rules, values)
            if len(possible_rules) == 1:
                possible_rules[0].row = i


def get_possible_rules(rules: list[Rule], values: list[int]) -> list[Rule]:
    possible_rules = [rule for rule in rules if rule.row is None]
    for value in values:
        matching_rules: list[Rule] = []
        for rule in possible_rules:
            if rule.matches(value):
                matching_rules.append(rule)
        possible_rules = matching_rules
    return possible_rules


if __name__ == "__main__":
    main()
