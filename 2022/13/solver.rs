use aoc_lib::answer;
use aoc_lib::reader::Reader;
use serde::Deserialize;
use std::cmp::Ordering;
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
    fn compare(&self, other: &Self) -> Ordering {
        match (self, other) {
            (PacketData::List(data_1), PacketData::List(data_2)) => {
                (0..data_1.len().min(data_2.len()))
                    .map(|i| data_1[i].compare(&data_2[i]))
                    .find(|&result| result != Ordering::Equal)
                    .unwrap_or(data_1.len().cmp(&data_2.len()))
            }
            (PacketData::Item(value_1), PacketData::Item(value_2)) => value_1.cmp(value_2),
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
    answer::timer(solution);
}

fn solution() {
    let packets: Vec<PacketData> = Reader::default()
        .read_lines()
        .iter()
        .filter(|line| !line.is_empty())
        .map(|line| line.parse().unwrap())
        .collect();
    answer::part1(4809, sum_adjacent(&packets));
    answer::part2(22600, get_decoder_key(&packets));
}

fn sum_adjacent(packets: &[PacketData]) -> usize {
    packets
        .chunks(2)
        .enumerate()
        .map(|(i, pair)| match pair[0].compare(&pair[1]) {
            Ordering::Less => i + 1,
            _ => 0,
        })
        .sum()
}

fn get_decoder_key(packets: &[PacketData]) -> usize {
    (packet_idx(packets, "[[2]]") + 1) * (packet_idx(packets, "[[6]]") + 2)
}

fn packet_idx(packets: &[PacketData], value: &str) -> usize {
    let target = value.parse::<PacketData>().unwrap();
    packets
        .iter()
        .filter(|packet| match target.compare(packet) {
            Ordering::Less => false,
            Ordering::Greater => true,
            Ordering::Equal => panic!("Should never be tied"),
        })
        .count()
}
