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

impl PacketData {
    fn from_string(value: &str) -> Self {
        serde_json::from_str(value).unwrap()
    }

    fn compare(&self, other: &Self) -> i8 {
        match (self, other) {
            (PacketData::List(data_1), PacketData::List(data_2)) => {
                for i in 0..data_1.len().min(data_2.len()) {
                    let result = data_1[i].compare(&data_2[i]);
                    if result != 0 {
                        return result;
                    }
                }
                if data_1.len() < data_2.len() {
                    -1
                } else if data_1.len() > data_2.len() {
                    1
                } else {
                    0
                }
            }
            (PacketData::Item(value_1), PacketData::Item(value_2)) => {
                if value_1 < value_2 {
                    -1
                } else if value_1 > value_2 {
                    1
                } else {
                    0
                }
            }
            (PacketData::List(data_1), item_2) => {
                PacketData::List(data_1.clone()).compare(&PacketData::List(vec![item_2.clone()]))
            }
            (item_1, PacketData::List(data_2)) => {
                PacketData::List(vec![item_1.clone()]).compare(&PacketData::List(data_2.clone()))
            }
        }
    }
}

fn main() {
    let packets: Vec<PacketData> = reader::read_lines()
        .iter()
        .filter(|line| !line.is_empty())
        .map(|line| PacketData::from_string(line))
        .collect();
    answer::part1(4809, sum_adjacent(&packets));
    answer::part2(22600, get_decoder_key(&packets));
}

fn sum_adjacent(packets: &Vec<PacketData>) -> usize {
    packets
        .chunks(2)
        .enumerate()
        .filter(|(_, pair)| {
            let packet_1 = &pair[0];
            let packet_2 = &pair[1];
            packet_1.compare(packet_2) < 0
        })
        .map(|(i, _)| i + 1)
        .sum()
}

fn get_decoder_key(packets: &Vec<PacketData>) -> usize {
    (packet_idx(packets, "[[2]]") + 1) * (packet_idx(packets, "[[6]]") + 2)
}

fn packet_idx(packets: &Vec<PacketData>, value: &str) -> usize {
    let target = PacketData::from_string(value);
    packets
        .iter()
        .filter(|packet| match target.compare(packet) {
            -1 => false,
            1 => true,
            _ => panic!("Should never be tied"),
        })
        .count()
}
