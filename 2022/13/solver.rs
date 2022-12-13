use aoc_lib::answer;
use aoc_lib::reader;
use serde::Deserialize;
use serde_json;

#[derive(Debug, PartialEq, Clone, Deserialize)]
#[serde(untagged)]
enum PacketData {
    Item(i64),
    List(Vec<PacketData>),
}

#[derive(Debug, PartialEq)]
enum Result {
    ORDERED,
    SWAPPED,
    TIED,
}

impl PacketData {
    fn compare(&self, other: &Self) -> Result {
        match (self, other) {
            (PacketData::List(data_1), PacketData::List(data_2)) => {
                for i in 0..data_1.len().min(data_2.len()) {
                    let result = data_1[i].compare(&data_2[i]);
                    if result != Result::TIED {
                        return result;
                    }
                }
                if data_1.len() < data_2.len() {
                    Result::ORDERED
                } else if data_1.len() > data_2.len() {
                    Result::SWAPPED
                } else {
                    Result::TIED
                }
            },
            (PacketData::Item(value_1), PacketData::Item(value_2)) => {
                if value_1 < value_2 {
                    Result::ORDERED
                } else if value_1 > value_2 {
                    Result::SWAPPED
                } else {
                    Result::TIED
                }
            },
            (PacketData::List(data_1), item_2) => {
                PacketData::List(data_1.clone())
                    .compare(&PacketData::List(vec![item_2.clone()]))
            },
            (item_1, PacketData::List(data_2)) => {
                PacketData::List(vec![item_1.clone()])
                    .compare(&PacketData::List(data_2.clone()))
            },
        }
    }
}

fn main() {
    let packets: Vec<PacketData> = reader::read_lines().iter()
        .filter(|line| !line.is_empty())
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    answer::part1(4809, sum_adjacent(&packets));
    answer::part2(22600, get_decoder_key(&packets));
}

fn sum_adjacent(packets: &Vec<PacketData>) -> usize {
    packets.chunks(2).enumerate()
        .filter(|(_, pair)| {
            let packet_1 = &pair[0];
            let packet_2 = &pair[1];
            let result = packet_1.compare(packet_2);
            result == Result::ORDERED
        })
        .map(|(i, _)| i + 1)
        .sum()
}

fn get_decoder_key(packets: &Vec<PacketData>) -> usize {
    let mut packets_copy: Vec<PacketData> = packets.clone();

    // Add in divider packets for part 2
    let div_1: PacketData = serde_json::from_str("[[2]]").unwrap();
    let div_2: PacketData = serde_json::from_str("[[6]]").unwrap();
    packets_copy.push(div_1.clone());
    packets_copy.push(div_2.clone());

    let ordered_packets = order_packets(&packets_copy);
    let index_1 = packet_index(&ordered_packets, &div_1);
    let index_2 = packet_index(&ordered_packets, &div_2);

    index_1 * index_2
}

fn packet_index(packets: &Vec<PacketData>, target: &PacketData) -> usize {
    packets.iter()
        .position(|packet| packet == target)
        .unwrap() + 1
}

fn order_packets(packets: &Vec<PacketData>) -> Vec<PacketData> {
    // Would avoid a lot of computation by doing a topological sort instead
    let mut result: Vec<PacketData> = Vec::new();
    let mut packets_copy = packets.clone();

    while !packets_copy.is_empty() {
        let index = get_next(&packets_copy);
        let packet = packets_copy.remove(index);
        result.push(packet);
    }

    result
}

fn get_next(packets: &Vec<PacketData>) -> usize {
    let options: Vec<usize> = (0..packets.len())
        .filter(|i| {
            let mut copied_packets: Vec<PacketData> = packets.clone();
            let base = copied_packets.remove(*i);

            let num_unordered = copied_packets.iter()
                .filter(|packet| base.compare(packet) != Result::ORDERED)
                .count();
            
            num_unordered == 0
        })
        .collect();
    
    if options.len() != 1 {
        panic!("Can't handle all these options: {:?}", options);
    }
    options[0]
}
