use aoc_lib::answer;
use aoc_lib::int_code::{Bus, Computer};
use aoc_lib::reader::Reader;
use std::collections::VecDeque;

#[derive(Debug, Clone)]
struct Packet {
    dest: usize,
    x: i64,
    y: i64,
}

#[derive(Debug)]
struct Network {
    nat: Option<Packet>,
    nodes: Vec<Node>,
}

impl Network {
    fn new(memory: Vec<i64>) -> Self {
        let nodes = (0..50)
            .map(|i| {
                let mut node = Node {
                    computer: Computer::new(NodeBus::new(i), memory.clone()),
                };
                let packets = node.run();
                assert_eq!(true, packets.is_empty());
                node
            })
            .collect();
        Self { nat: None, nodes }
    }

    fn run_until_repeat(&mut self) -> Vec<i64> {
        let mut history = Vec::new();
        loop {
            let packets: Vec<Packet> = self.nodes.iter_mut().flat_map(|node| node.run()).collect();
            packets.iter().for_each(|packet| self.send_packet(packet));
            if packets.is_empty() {
                let nat = self.nat.as_ref().unwrap().clone();
                let destination = nat.y;
                let seen = history.contains(&destination);
                history.push(destination);
                if seen {
                    return history;
                }
                self.send_packet(&Packet {
                    dest: 0,
                    x: nat.x,
                    y: nat.y,
                });
            }
        }
    }

    fn send_packet(&mut self, packet: &Packet) {
        if packet.dest == 255 {
            self.nat = Some(packet.clone());
        } else {
            let node = &mut self.nodes[packet.dest];
            node.send_packet(packet);
        }
    }
}

#[derive(Debug)]
struct Node {
    computer: Computer<NodeBus>,
}

impl Node {
    fn run(&mut self) -> Vec<Packet> {
        self.computer.bus.running = true;
        self.computer.run();
        self.computer.bus.pull_packets()
    }

    fn send_packet(&mut self, packet: &Packet) {
        self.computer.bus.send_packet(packet);
    }
}

#[derive(Debug)]
struct NodeBus {
    packets: VecDeque<i64>,
    running: bool,
    buffer: Vec<i64>,
    outbound_packets: Vec<Packet>,
}

impl NodeBus {
    fn new(id: i64) -> Self {
        Self {
            packets: [id].into(),
            running: true,
            buffer: Vec::new(),
            outbound_packets: Vec::new(),
        }
    }

    fn pull_packets(&mut self) -> Vec<Packet> {
        let packets = self.outbound_packets.clone();
        self.outbound_packets.clear();
        packets
    }

    fn send_packet(&mut self, packet: &Packet) {
        self.packets.push_back(packet.x);
        self.packets.push_back(packet.y);
    }
}

impl Bus for NodeBus {
    fn active(&self) -> bool {
        self.running
    }

    fn get_input(&mut self) -> i64 {
        if self.packets.is_empty() {
            self.running = false;
            -1
        } else {
            self.packets.pop_front().unwrap()
        }
    }

    fn add_output(&mut self, value: i64) {
        self.buffer.push(value);
        if self.buffer.len() == 3 {
            let dest = self.buffer[0] as usize;
            let (x, y) = (self.buffer[1], self.buffer[2]);
            self.buffer.clear();
            self.outbound_packets.push(Packet { dest, x, y });
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut network = Network::new(Reader::default().read_csv());
    let history = network.run_until_repeat();
    answer::part1(16549, *history.first().unwrap());
    answer::part2(11462, *history.last().unwrap());
}
