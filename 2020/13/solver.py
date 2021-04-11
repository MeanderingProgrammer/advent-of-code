import math

from commons.aoc_parser import Parser


class Bus:

    def __init__(self, bus_id):
        self.real = bus_id != 'x'
        if self.real:
            self.bus_id = int(bus_id)

    def get_wait_time(self, arrive_time):
        if not self.real:
            return math.inf
        interval = self.bus_id
        late_time = arrive_time % interval
        time_to_wait = interval - late_time
        return time_to_wait % interval


def main():
    data = process()

    arrive_time = int(data[0])
    buses = [Bus(bus) for bus in data[1].split(',')]

    # Part 1: 296
    print('Part 1: {}'.format(solve_part_1(arrive_time, buses)))
    # Part 2: 535296695251210
    print('Part 2: {}'.format(solve_part_2(buses)))


def solve_part_1(arrive_time, buses):
    wait_times = [bus.get_wait_time(arrive_time) for bus in buses]
    min_wait_times = min(wait_times)
    bus = buses[wait_times.index(min_wait_times)]
    return bus.bus_id * min_wait_times


def solve_part_2(buses):
    # Uses CRT: https://brilliant.org/wiki/chinese-remainder-theorem/
    multiple = get_multiple(buses)
    total = 0
    for i, bus in enumerate(buses):
        if bus.real:
            n = bus.bus_id
            a = (n - i) % n
            y = multiple // n
            z = get_inverse_mod(y, n)
            total += (a*y*z)
    return total % multiple


def get_multiple(buses):
    result = 1
    for bus in buses:
        if bus.real:
            result *= bus.bus_id
    return result


def get_inverse_mod(y, n):
    for i in range(1, n):
        if (y * i) % n == 1:
            return i
    return None


def brute_force_2(buses):
    intervals = [bus.bus_id if bus.real else 0 for bus in buses]
    max_interval = max(intervals)
    max_offset = intervals.index(max_interval)
    return find_start_time(buses, max_interval, max_offset)


def find_start_time(buses, interval, offset):
    index = 1
    while True:
        start_time = (interval * index) - offset
        if consecutive_from_start(start_time, buses):
            return start_time
        index += 1


def consecutive_from_start(start_time, buses):
    for i, bus in enumerate(buses):
        if bus.real:
            if bus.get_wait_time(start_time) != i:
                return False
    return True


def process():
   return Parser().lines()


if __name__ == '__main__':
    main()
