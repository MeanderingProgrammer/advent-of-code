from commons.aoc_parser import Parser
from commons.int_code import Computer


class Network:

    def __init__(self, memory):
        self.__nat = None
        self.__nat_history = []

        self.__network = {}

        for i in range(50):
            node = Node([value for value in memory], i, self)
            self.__network[i] = node
            node.run()

    def run_until_nat_repeat(self):
        while True:
            running = True
            for i in range(50):
                self.__network[i].run()
                running = running and self.__network[i].running
            if not running:
                destination = self.__nat.y

                if destination in self.__nat_history:
                    self.__nat_history.append(destination)
                    return self.__nat_history

                self.__nat_history.append(destination)
                self.__send_to_node(self.__network[0], self.__nat)

    def send_packet(self, packet):
        if packet.dest == 255:
            self.__nat = packet
        else:
            destination = self.__network[packet.dest]
            self.__send_to_node(destination, packet)

    @staticmethod
    def __send_to_node(node, packet):
        node.packets.append(packet.x)
        node.packets.append(packet.y)
        node.run()


class Node:

    def __init__(self, memory, address, network):
        self.__computer = Computer(self)
        self.__computer.set_memory(memory)
        self.__network = network
        self.__address = address

        self.packets = [address]
        self.running = True
        self.__send = []

    def run(self):
        self.running = True
        while self.__computer.has_next() and self.running:
            self.__computer.next()

    def get_input(self):
        if len(self.packets) == 0:
            self.running = False
            return -1
        else:
            return self.packets.pop(0)

    def add_output(self, value):
        self.__send.append(value)
        if len(self.__send) == 3:
            self.__network.send_packet(Packet(*self.__send))
            self.__send = []


class Packet:

    def __init__(self, dest, x, y):
        self.dest, self.x, self.y = dest, x, y

    def __str__(self):
        return 'To: {}, X={}, Y={}'.format(self.dest, self.x, self.y)


def main():
    network = Network(get_memory())
    nat_history = network.run_until_nat_repeat()
    # Part 1: 16549
    print('Part 1: {}'.format(nat_history[0]))
    # Part 2: 11462
    print('Part 2: {}'.format(nat_history[-1]))


def get_memory():
    return Parser().int_csv()


if __name__ == '__main__':
    main()
