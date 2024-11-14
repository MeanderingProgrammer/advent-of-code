use aoc_lib::answer;
use aoc_lib::reader::Reader;
use rayon::prelude::*;
use std::collections::VecDeque;

#[derive(Debug, Clone)]
struct HashInfo {
    i: usize,
    triple: u8,
    cinqs: Vec<u8>,
}

#[derive(Debug)]
struct Hasher {
    prefix: String,
    n: usize,
}

impl Hasher {
    fn new(prefix: String, n: usize) -> Self {
        Self { prefix, n }
    }

    fn compute_range(&self, start: usize, end: usize) -> VecDeque<HashInfo> {
        if self.n == 0 || end - start == 0 {
            (start..=end).filter_map(|i| self.compute(i)).collect()
        } else {
            (start..=end)
                .into_par_iter()
                .filter_map(|i| self.compute(i))
                .collect()
        }
    }

    fn compute(&self, i: usize) -> Option<HashInfo> {
        let mut digest = md5::compute(format!("{}{i}", self.prefix));
        let mut hash = [0; 32];
        for _ in 0..(self.n) {
            Self::fill_hash(&mut hash, digest);
            digest = md5::compute(hash);
        }
        Self::fill_hash(&mut hash, digest);
        Self::repeats(&hash, 3).first().map(|&triple| HashInfo {
            i,
            triple,
            cinqs: Self::repeats(&hash, 5),
        })
    }

    fn fill_hash(buffer: &mut [u8; 32], digest: md5::Digest) {
        for i in 0..16 {
            let ch = digest[i];
            let (v1, v2) = (ch >> 4, ch & 0xf);
            buffer[i * 2] = Self::hex_ascii(v1);
            buffer[i * 2 + 1] = Self::hex_ascii(v2);
        }
    }

    fn hex_ascii(ch: u8) -> u8 {
        let offset = if ch < 10 { 48 } else { 87 };
        offset + ch
    }

    fn repeats(hash: &[u8; 32], size: usize) -> Vec<u8> {
        let mut result = Vec::new();
        let mut start = 0;
        for i in 1..hash.len() {
            if hash[i] == hash[start] {
                if i - start == size - 1 {
                    result.push(hash[i]);
                }
            } else {
                start = i;
            }
        }
        result
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let prefix = Reader::default().read_line();
    answer::part1(15168, generate(&prefix, 0));
    answer::part2(20864, generate(&prefix, 2_016));
}

fn generate(prefix: &str, n: usize) -> usize {
    let hasher = Hasher::new(prefix.to_string(), n);

    let mut hashes = VecDeque::new();
    let mut i = 0;
    while hashes.is_empty() {
        if let Some(hash) = hasher.compute(i) {
            hashes.push_back(hash);
        }
        i += 1;
    }

    let mut keys = Vec::new();
    while keys.len() < 64 {
        let hash = hashes.pop_front().unwrap();
        let end = hash.i + 1_000;

        hashes.append(&mut hasher.compute_range(i, end));

        for other in hashes.iter() {
            if end < other.i {
                break;
            }
            if other.cinqs.contains(&hash.triple) {
                keys.push(hash.i);
                break;
            }
        }

        i = end + 1;
    }
    *keys.last().unwrap()
}
