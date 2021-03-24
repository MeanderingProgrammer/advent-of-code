import math

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

    #solve_part_1(arrive_time, buses)
    solve_part_2(buses)


def solve_part_1(arrive_time, buses):
    # Result = 296
    wait_times = [bus.get_wait_time(arrive_time) for bus in buses]
    min_wait_times = min(wait_times)
    bus = buses[wait_times.index(min_wait_times)]
    print('Bus * Wait Time = {}'.format(bus.bus_id * min_wait_times))


def solve_part_2(buses):
    # Result = 
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
    result = total % multiple
    print('First consecutive start time = {}'.format(result))


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

    start_time = find_start_time(buses, max_interval, max_offset)
    print('First consecutive start time = {}'.format(start_time))


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
    with open('data.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    main()

