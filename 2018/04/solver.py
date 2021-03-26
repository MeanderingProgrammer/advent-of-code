import re

from aoc_parser import Parser


EVENT_PATTERN = '^\[(.*)-(.*)-(.*) (.*):(.*)\] (.*)$'


class Event:

    def __init__(self, value):
        match = re.match(EVENT_PATTERN, value)
        self.minute = int(match[5])
        self.name = match[6]

    def guard_id(self):
        parts = self.name.split()
        return int(parts[1][1:]) if parts[0] == 'Guard' else None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {}'.format(self.minute, self.name)


class TimeRange:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def minutes(self):
        return range(self.start, self.end)

    def __len__(self):
        return self.end - self.start

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} - {}'.format(self.start, self.end)


class GuardEvents:

    def __init__(self):
        self.time_ranges = []
        self.start = None

    def add(self, event):
        if self.start is None:
            self.start = event.minute
        else:
            time_range = TimeRange(self.start, event.minute)
            self.time_ranges.append(time_range)
            self.start = None

    def get_sleep_time(self):
        return sum([len(time_range) for time_range in self.time_ranges])

    def get_minute_frequencies(self):
        minute_frequencies = {}
        for time_range in self.time_ranges:
            for minute in time_range.minutes():
                if minute not in minute_frequencies:
                    minute_frequencies[minute] = 0
                minute_frequencies[minute] += 1
        return minute_frequencies

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.time_ranges)


def main():
    guard_events = {}
    guard_id = None

    for line in sorted(Parser('data').lines()):
        event = Event(line)
        if event.guard_id() is not None:
            guard_id = event.guard_id()
        else:
            if guard_id not in guard_events:
                guard_events[guard_id] = GuardEvents()
            guard_events[guard_id].add(event)

    # Part 1: 48680
    print('Part 1: {}'.format(solve_strategy_1(guard_events)))
    # Part 2: 94826
    print('Part 2: {}'.format(solve_strategy_2(guard_events)))


def solve_strategy_1(guard_events):
    guard_ids = [guard_id for guard_id in guard_events]
    guard_ids = sorted(guard_ids, key=lambda guard_id: guard_events[guard_id].get_sleep_time())

    sleepiest_guard, sleepiest_events = guard_ids[-1], guard_events[guard_ids[-1]]
    
    minute_frequencies = sleepiest_events.get_minute_frequencies()
    minutes = [minute for minute in minute_frequencies]
    minutes = sorted(minutes, key=lambda minute: minute_frequencies[minute])
    most_common_minute = minutes[-1]

    return sleepiest_guard * most_common_minute


def solve_strategy_2(guard_events):
    
    chosen_guard, chosen_minute, frequncy = None, None, 0
    for guard_id in guard_events:
        events = guard_events[guard_id]

        minute_frequencies = events.get_minute_frequencies()
        minutes = [minute for minute in minute_frequencies]
        minutes = sorted(minutes, key=lambda minute: minute_frequencies[minute])

        most_common_minute, most_common_minute_frequency = minutes[-1], minute_frequencies[minutes[-1]]

        if most_common_minute_frequency > frequncy:
            chosen_guard, chosen_minute, frequncy = guard_id, most_common_minute, most_common_minute_frequency

    return chosen_guard * chosen_minute


if __name__ == '__main__':
    main()
