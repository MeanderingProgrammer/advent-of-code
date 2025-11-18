from dataclasses import dataclass, field

from aoc import answer
from aoc.intcode import Computer
from aoc.parser import Parser


@dataclass(frozen=True)
class Packet:
    dest: int
    x: int
    y: int


class Network:
    def __init__(self, memory: list[int]):
        self.nat: Packet | None = None
        self.network: list[Node] = [
            Node(Computer(bus=NodeBus(network=self, packets=[i]), memory=memory.copy()))
            for i in range(50)
        ]

    def run_until_repeat(self) -> list[int]:
        history: list[int] = []
        self.run()
        while True:
            self.run()
            assert self.nat is not None
            destination = self.nat.y
            seen = destination in history
            history.append(destination)
            if seen:
                return history
            self.send_packet(Packet(dest=0, x=self.nat.x, y=self.nat.y))

    def run(self) -> None:
        [node.run() for node in self.network]

    def send_packet(self, packet: Packet) -> None:
        if packet.dest == 255:
            self.nat = packet
        else:
            node = self.network[packet.dest]
            node.send_packet(packet)
            node.run()


@dataclass(frozen=True)
class Node:
    computer: Computer["NodeBus"]

    def run(self) -> None:
        self.computer.bus.running = True
        self.computer.run()

    def send_packet(self, packet: Packet) -> None:
        self.computer.bus.send_packet(packet)


@dataclass
class NodeBus:
    network: Network
    packets: list[int]
    running: bool = True
    buffer: list[int] = field(default_factory=list)

    def send_packet(self, packet: Packet) -> None:
        self.packets.append(packet.x)
        self.packets.append(packet.y)

    def active(self) -> bool:
        return self.running

    def get_input(self) -> int:
        if len(self.packets) == 0:
            self.running = False
            return -1
        else:
            return self.packets.pop(0)

    def add_output(self, value: int) -> None:
        self.buffer.append(value)
        if len(self.buffer) == 3:
            dest, x, y = self.buffer
            self.buffer.clear()
            self.network.send_packet(Packet(dest=dest, x=x, y=y))


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    network = Network(memory)
    history = network.run_until_repeat()
    answer.part1(16549, history[0])
    answer.part2(11462, history[-1])


if __name__ == "__main__":
    main()
