from dataclasses import dataclass
from typing import Optional

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Bus:
    interval: Optional[int]

    def wait_time(self, arrival: int) -> Optional[int]:
        if self.interval is None:
            return None
        late_time = arrival % self.interval
        time_to_wait = self.interval - late_time
        return time_to_wait % self.interval


def main():
    raw_arrival, raw_buses = Parser().lines()
    arrival, buses = int(raw_arrival), get_buses(raw_buses)
    answer.part1(296, solve_part_1(buses, arrival))
    answer.part2(535296695251210, solve_part_2(buses))


def get_buses(raw_buses: str) -> list[Bus]:
    return [Bus(None if raw == "x" else int(raw)) for raw in raw_buses.split(",")]


def solve_part_1(buses: list[Bus], arrival: int) -> int:
    wait_times = [bus.wait_time(arrival) for bus in buses]
    min_wait_times = min(
        [wait_time for wait_time in wait_times if wait_time is not None]
    )
    bus = buses[wait_times.index(min_wait_times)]
    assert bus.interval is not None
    return bus.interval * min_wait_times


def solve_part_2(buses: list[Bus]) -> int:
    # Uses CRT: https://brilliant.org/wiki/chinese-remainder-theorem/
    total = 0
    multiple = get_multiple(buses)
    for i, bus in enumerate(buses):
        if bus.interval is not None:
            n = bus.interval
            a = (n - i) % n
            y = multiple // n
            z = get_inverse_mod(y, n)
            total += a * y * z
    return total % multiple


def get_multiple(buses: list[Bus]) -> int:
    result: int = 1
    for bus in buses:
        if bus.interval is not None:
            result *= bus.interval
    return result


def get_inverse_mod(y: int, n: int) -> int:
    for i in range(1, n):
        if (y * i) % n == 1:
            return i
    raise Exception("Failed")


if __name__ == "__main__":
    main()
