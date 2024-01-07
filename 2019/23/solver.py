from dataclasses import dataclass, field
from typing import Optional, override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


@dataclass(frozen=True)
class Packet:
    dest: int
    x: int
    y: int


class Network:
    def __init__(self, memory: list[int]):
        self.nat: Optional[Packet] = None
        self.network: list[Node] = [
            Node(Computer(bus=NodeBus(network=self, packets=[i]), memory=list(memory)))
            for i in range(50)
        ]
        [node.run() for node in self.network]

    def run_until_repeat(self) -> list[int]:
        history: list[int] = []
        while True:
            running = all([node.run() for node in self.network])
            if running:
                continue
            assert self.nat is not None
            destination = self.nat.y
            seen = destination in history
            history.append(destination)
            if seen:
                return history
            self.send_to_node(0, self.nat)

    def send_packet(self, packet: Packet) -> None:
        if packet.dest == 255:
            self.nat = packet
        else:
            self.send_to_node(packet.dest, packet)

    def send_to_node(self, destination: int, packet: Packet) -> None:
        node = self.network[destination]
        node.send_packet(packet)
        node.run()


@dataclass(frozen=True)
class Node:
    computer: Computer

    def run(self) -> bool:
        self.computer.bus.running = True
        self.computer.run()
        return self.computer.bus.active()

    def send_packet(self, packet: Packet) -> None:
        self.computer.bus.packets.append(packet.x)
        self.computer.bus.packets.append(packet.y)


@dataclass
class NodeBus(Bus):
    network: Network
    packets: list[int]
    running: bool = True
    buffer: list[int] = field(default_factory=list)

    @override
    def active(self) -> bool:
        return self.running

    @override
    def get_input(self) -> int:
        if len(self.packets) == 0:
            self.running = False
            return -1
        else:
            return self.packets.pop(0)

    @override
    def add_output(self, value: int) -> None:
        self.buffer.append(value)
        if len(self.buffer) == 3:
            dest, x, y = self.buffer
            self.buffer.clear()
            self.network.send_packet(Packet(dest=dest, x=x, y=y))


@answer.timer
def main() -> None:
    network = Network(Parser().int_csv())
    history = network.run_until_repeat()
    answer.part1(16549, history[0])
    answer.part2(11462, history[-1])


if __name__ == "__main__":
    main()
