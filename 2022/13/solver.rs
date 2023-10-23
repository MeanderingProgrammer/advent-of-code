use aoc_lib::answer;
use aoc_lib::reader;
use serde::Deserialize;
use serde_json;
use std::str::FromStr;

#[derive(Debug, PartialEq, Clone, Deserialize)]
#[serde(untagged)]
enum PacketData {
    Item(i64),
    List(Vec<PacketData>),
}

impl FromStr for PacketData {
    type Err = serde_json::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        serde_json::from_str(s)
    }
}

impl PacketData {
    fn compare(&self, other: &Self) -> i8 {
        match (self, other) {
            (PacketData::List(data_1), PacketData::List(data_2)) => {
                for i in 0..data_1.len().min(data_2.len()) {
                    let result = data_1[i].compare(&data_2[i]);
                    if result != 0 {
                        return result;
                    }
                }
                Self::int_compare(data_1.len() as i64, data_2.len() as i64)
            }
            (PacketData::Item(value_1), PacketData::Item(value_2)) => {
                Self::int_compare(*value_1, *value_2)
            }
            (PacketData::List(data_1), item_2) => {
                PacketData::List(data_1.clone()).compare(&PacketData::List(vec![item_2.clone()]))
            }
            (item_1, PacketData::List(data_2)) => {
                PacketData::List(vec![item_1.clone()]).compare(&PacketData::List(data_2.clone()))
            }
        }
    }

    fn int_compare(v1: i64, v2: i64) -> i8 {
        match v1.cmp(&v2) {
            std::cmp::Ordering::Less => -1,
            std::cmp::Ordering::Equal => 0,
            std::cmp::Ordering::Greater => 1,
        }
    }
}

fn main() {
    let packets: Vec<PacketData> = reader::read_lines()
        .iter()
        .filter(|line| !line.is_empty())
        .map(|line| line.parse().unwrap())
        .collect();
    answer::part1(4809, sum_adjacent(&packets));
    answer::part2(22600, get_decoder_key(&packets));
}

fn sum_adjacent(packets: &Vec<PacketData>) -> usize {
    packets
        .chunks(2)
        .enumerate()
        .filter(|(_, pair)| pair[0].compare(&pair[1]) < 0)
        .map(|(i, _)| i + 1)
        .sum()
}

fn get_decoder_key(packets: &Vec<PacketData>) -> usize {
    (packet_idx(packets, "[[2]]") + 1) * (packet_idx(packets, "[[6]]") + 2)
}

fn packet_idx(packets: &Vec<PacketData>, value: &str) -> usize {
    let target = value.parse::<PacketData>().unwrap();
    packets
        .iter()
        .filter(|packet| match target.compare(packet) {
            -1 => false,
            1 => true,
            _ => panic!("Should never be tied"),
        })
        .count()
}
