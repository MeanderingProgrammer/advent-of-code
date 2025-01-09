use aoc_lib::answer;
use aoc_lib::reader::Reader;
use rayon::prelude::*;
use std::collections::VecDeque;

#[derive(Debug, Clone)]
struct HashInfo {
    i: usize,
    triple: u8,
    quintuple: Option<u8>,
}

#[derive(Debug)]
struct Hasher {
    prefix: String,
    n: usize,
    batch: usize,
}

impl Hasher {
    fn new(prefix: String, n: usize, batch: usize) -> Self {
        Self { prefix, n, batch }
    }

    fn compute_range(&self, start: usize, end: usize) -> (usize, VecDeque<HashInfo>) {
        let end = end.max(start + self.batch) + 1;
        (
            end,
            (start..end)
                .into_par_iter()
                .filter_map(|i| self.compute(i))
                .collect(),
        )
    }

    fn compute(&self, i: usize) -> Option<HashInfo> {
        let mut digest = md5::compute(format!("{}{i}", self.prefix));
        let mut hash = [0; 32];
        for _ in 0..(self.n) {
            Self::fill_hash(&mut hash, digest);
            digest = md5::compute(hash);
        }
        Self::fill_hash(&mut hash, digest);
        Self::repeat(&hash, 3).map(|triple| HashInfo {
            i,
            triple,
            quintuple: Self::repeat(&hash, 5),
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

    fn repeat(hash: &[u8; 32], size: usize) -> Option<u8> {
        hash.windows(size).find_map(|window| {
            let first = window[0];
            if window.iter().all(|&ch| ch == first) {
                Some(first)
            } else {
                None
            }
        })
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
    let hasher = Hasher::new(prefix.to_string(), n, 1_000);

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
        let hash_end = hash.i + 1_000;

        if i <= hash_end {
            let (next_start, mut more_hashes) = hasher.compute_range(i, hash_end);
            i = next_start;
            hashes.append(&mut more_hashes);
        }

        for other in hashes.iter() {
            if other.i > hash_end {
                break;
            }
            if other.quintuple == Some(hash.triple) {
                keys.push(hash.i);
                break;
            }
        }
    }
    *keys.last().unwrap()
}
