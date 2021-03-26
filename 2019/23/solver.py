from computer import Computer

DEBUG = False



class Network:

    def __init__(self, memory):
        self.__nat = None
        self.__network = {}
        for i in range(50):
            node = Node([value for value in memory], i, self)
            self.__network[i] = node
            node.run()

        while True:
            running = True
            for i in range(50):
                self.__network[i].run()
                running = running and self.__network[i].running
            if not running:
                print(self.__nat)
                self.__send_to_node(self.__network[0], self.__nat)

    def send_packet(self, packet):
        print(packet)
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
        self.__computer = Computer(self, DEBUG)
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


def get_memory():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        return [int(datum) for datum in f.read().split(',')]


if __name__ == '__main__':
    main()
