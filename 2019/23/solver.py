from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


class Network:
    def __init__(self, memory: list[int]):
        self.nat = None
        self.nat_history = []

        self.network = {}
        for i in range(50):
            node = Node(list(memory), i, self)
            self.network[i] = node
            node.run()

    def run_until_nat_repeat(self):
        while True:
            running = True
            for i in range(50):
                self.network[i].run()
                running = running and self.network[i].running
            if not running:
                destination = self.nat.y
                if destination in self.nat_history:
                    self.nat_history.append(destination)
                    return self.nat_history
                self.nat_history.append(destination)
                Network.send_to_node(self.network[0], self.nat)

    def send_packet(self, packet):
        if packet.dest == 255:
            self.nat = packet
        else:
            destination = self.network[packet.dest]
            Network.send_to_node(destination, packet)

    @staticmethod
    def send_to_node(node, packet):
        node.packets.append(packet.x)
        node.packets.append(packet.y)
        node.run()


class Node(Bus):
    def __init__(self, memory: list[int], address, network):
        self.computer = Computer(bus=self, memory=memory)
        self.network = network

        self.packets = [address]
        self.running = True
        self.send = []

    def run(self) -> None:
        self.running = True
        self.computer.run()

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
        self.send.append(value)
        if len(self.send) == 3:
            self.network.send_packet(Packet(*self.send))
            self.send = []


class Packet:
    def __init__(self, dest, x, y):
        self.dest, self.x, self.y = dest, x, y

    def __str__(self):
        return "To: {}, X={}, Y={}".format(self.dest, self.x, self.y)


def main() -> None:
    network = Network(Parser().int_csv())
    nat_history = network.run_until_nat_repeat()
    answer.part1(16549, nat_history[0])
    answer.part2(11462, nat_history[-1])


if __name__ == "__main__":
    main()
