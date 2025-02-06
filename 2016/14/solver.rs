use aoc::{answer, Md5, Reader};
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
        let end = end.max(start + self.batch);
        (
            end,
            (start..end)
                .into_par_iter()
                .step_by(8)
                .flat_map(|i| self.compute(i))
                .collect(),
        )
    }

    fn compute(&self, start: usize) -> VecDeque<HashInfo> {
        let inputs = std::array::from_fn(|i| format!("{}{}", self.prefix, start + i));
        let mut digests = Md5::from(inputs).compute();
        for _ in 0..(self.n) {
            digests = Md5::from(digests).compute();
        }
        Md5::from(digests)
            .buffers
            .into_iter()
            .enumerate()
            .filter_map(|(i, hash)| {
                let hash = &hash[0..32];
                Self::repeat(hash, 3).map(|triple| HashInfo {
                    i: start + i,
                    triple,
                    quintuple: Self::repeat(hash, 5),
                })
            })
            .collect()
    }

    fn repeat(hash: &[u8], size: usize) -> Option<u8> {
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
    let prefix: String = Reader::default().line();
    answer::part1(15168, generate(&prefix, 0));
    answer::part2(20864, generate(&prefix, 2_016));
}

fn generate(prefix: &str, n: usize) -> usize {
    let hasher = Hasher::new(prefix.to_string(), n, 1_000);

    let mut hashes = VecDeque::default();
    let mut i = 0;
    while hashes.is_empty() {
        hashes.append(&mut hasher.compute(i));
        i += 8;
    }

    let mut keys = Vec::default();
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
