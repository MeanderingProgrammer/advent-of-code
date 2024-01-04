from dataclasses import dataclass
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
        self.network: list[Node] = [Node(list(memory), i, self) for i in range(50)]
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


class Node(Bus):
    def __init__(self, memory: list[int], address: int, network: Network):
        self.computer: Computer = Computer(bus=self, memory=memory)
        self.network: Network = network
        self.packets: list[int] = [address]
        self.running: bool = True
        self.buffer: list[int] = []

    def run(self) -> bool:
        self.running = True
        self.computer.run()
        return self.running

    def send_packet(self, packet: Packet) -> None:
        self.packets.append(packet.x)
        self.packets.append(packet.y)

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
            packet = Packet(dest=self.buffer[0], x=self.buffer[1], y=self.buffer[2])
            self.buffer.clear()
            self.network.send_packet(packet)


@answer.timer
def main() -> None:
    network = Network(Parser().int_csv())
    history = network.run_until_repeat()
    answer.part1(16549, history[0])
    answer.part2(11462, history[-1])


if __name__ == "__main__":
    main()
