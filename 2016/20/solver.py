from aoc import answer
from aoc.parser import Parser


class DataRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def can_join(self, o):
        starts_before = self.start <= o.start
        if starts_before:
            return o.start <= self.end
        else:
            return o.can_join(self)

    def join(self, os):
        data_ranges = os + [self]
        starts = [data_range.start for data_range in data_ranges]
        ends = [data_range.end for data_range in data_ranges]
        return DataRange(min(starts), max(ends))

    def __lt__(self, o):
        return self.start < o.start

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "[{}, {}]".format(self.start, self.end)


def main():
    data_ranges = get_data_ranges()
    data_ranges = combine_all(data_ranges)
    data_ranges.sort()

    answer.part1(17348574, data_ranges[0].end + 1)
    answer.part2(104, get_total_unblocked(data_ranges))


def combine_all(data_ranges):
    can_combine = True
    while can_combine:
        data_ranges, can_combine = combine(data_ranges)
    return data_ranges


def combine(data_ranges):
    new_ranges, joined, combined = [], set(), False
    for data_range in data_ranges:
        if data_range in joined:
            continue

        matches = get_matches(data_range, data_ranges)

        joined.add(data_range)
        for match in matches:
            joined.add(match)

        if len(matches) > 0:
            combined = True
            new_ranges.append(data_range.join(matches))
        else:
            new_ranges.append(data_range)

    return new_ranges, combined


def get_matches(data_range, data_ranges):
    matches = []
    for other_range in data_ranges:
        if other_range != data_range and data_range.can_join(other_range):
            matches.append(other_range)
    return matches


def get_total_unblocked(data_ranges):
    total = 0
    for i, data_range in enumerate(data_ranges[:-1]):
        next_data_range = data_ranges[i + 1]
        total += count_between(data_range, next_data_range)
    return total


def count_between(prev_range, next_range):
    end = prev_range.end
    start = next_range.start
    return start - end - 1


def get_data_ranges():
    data_ranges = []
    for line in Parser().lines():
        line = line.split("-")
        data_ranges.append(DataRange(int(line[0]), int(line[1])))
    return data_ranges


if __name__ == "__main__":
    main()
