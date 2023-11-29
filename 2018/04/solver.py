import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Event:
    minute: int
    name: str

    def guard_id(self):
        parts = self.name.split()
        return int(parts[1][1:]) if parts[0] == "Guard" else None


@dataclass(frozen=True)
class TimeRange:
    start: int
    end: int

    def minutes(self) -> list[int]:
        return list(range(self.start, self.end))

    def __len__(self):
        return self.end - self.start


@dataclass
class GuardEvents:
    time_ranges: list[TimeRange]
    start: Optional[int] = None

    def add(self, event: Event) -> None:
        if self.start is None:
            self.start = event.minute
        else:
            time_range = TimeRange(start=self.start, end=event.minute)
            self.time_ranges.append(time_range)
            self.start = None

    def get_sleep_time(self) -> int:
        return sum([len(time_range) for time_range in self.time_ranges])

    def most_common(self) -> tuple[int, int]:
        minute_frequencies = self.get_minute_frequencies()
        minutes = [minute for minute in minute_frequencies]
        minutes = sorted(minutes, key=lambda minute: minute_frequencies[minute])
        return minutes[-1], minute_frequencies[minutes[-1]]

    def get_minute_frequencies(self) -> dict[int, int]:
        minute_frequencies: dict[int, int] = defaultdict(int)
        for time_range in self.time_ranges:
            for minute in time_range.minutes():
                minute_frequencies[minute] += 1
        return minute_frequencies


def main() -> None:
    guard_events = get_guard_events()
    answer.part1(48680, solve_strategy_1(guard_events))
    answer.part2(94826, solve_strategy_2(guard_events))


def get_guard_events() -> dict[int, GuardEvents]:
    def parse_event(line: str) -> Event:
        match = re.match(r"^\[(.*)-(.*)-(.*) (.*):(.*)\] (.*)$", line)
        assert match is not None
        return Event(
            minute=int(match[5]),
            name=match[6],
        )

    guard_events: dict[int, GuardEvents] = dict()
    guard_id = None
    for line in sorted(Parser().lines()):
        event = parse_event(line)
        if event.guard_id() is not None:
            guard_id = event.guard_id()
        else:
            assert guard_id is not None
            if guard_id not in guard_events:
                guard_events[guard_id] = GuardEvents(time_ranges=[])
            guard_events[guard_id].add(event)
    return guard_events


def solve_strategy_1(guard_events: dict[int, GuardEvents]) -> int:
    guard_ids = [guard_id for guard_id in guard_events]
    guard_ids = sorted(
        guard_ids, key=lambda guard_id: guard_events[guard_id].get_sleep_time()
    )
    sleepiest_guard = guard_ids[-1]
    most_common_minute, _ = guard_events[sleepiest_guard].most_common()
    return sleepiest_guard * most_common_minute


def solve_strategy_2(guard_events: dict[int, GuardEvents]) -> int:
    chosen_guard = None
    chosen_minute = None
    frequncy = 0
    for guard_id, events in guard_events.items():
        most_common_minute, most_common_frequency = events.most_common()
        if most_common_frequency > frequncy:
            chosen_guard = guard_id
            chosen_minute = most_common_minute
            frequncy = most_common_frequency
    assert chosen_guard is not None and chosen_minute is not None
    return chosen_guard * chosen_minute


if __name__ == "__main__":
    main()
