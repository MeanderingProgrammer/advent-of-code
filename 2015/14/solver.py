from aoc_parser import Parser


FILE_NAME = 'data'
TIME = 2_503


class Reindeer:

    def __init__(self, raw):
        parts = raw.split()
        self.speed = int(parts[3])
        self.time = int(parts[6])
        self.rest = int(parts[13])

    def distance(self, elapsed_time):
        cycle = self.time + self.rest
        complete = elapsed_time // cycle
        remainder = elapsed_time % cycle
        remainder_at_speed = min(remainder, self.time)
        total_seconds_at_speed = (complete * self.time) + remainder_at_speed
        return self.speed * total_seconds_at_speed
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} km/s for {}, rest {}'.format(self.speed, self.time, self.rest)


def main():
    reindeers = get_reindeers()
    # Part 1 = 2655
    print('Part 1: {}'.format(max(get_distance_after(reindeers, TIME))))
    # Part 2 = 1059
    print('Part 2: {}'.format(max(get_times_in_lead(reindeers))))


def get_times_in_lead(reindeers):
    times_in_lead = [0] * len(reindeers)
    for seconds in range(1, TIME + 1):
        distances = get_distance_after(reindeers, seconds)
        indexes = indexes_of_max(distances)
        for index in indexes:
            times_in_lead[index] += 1
    return times_in_lead


def get_distance_after(reindeers, time):
    distances = []
    for reindeer in reindeers:
        distances.append(reindeer.distance(time))
    return distances


def indexes_of_max(values):
    indexes = []
    maximum_value = max(values)
    for i, value in enumerate(values):
        if value == maximum_value:
            indexes.append(i)
    return indexes


def get_reindeers():
    return [Reindeer(line) for line in Parser(FILE_NAME).lines()]


if __name__ == '__main__':
    main()
