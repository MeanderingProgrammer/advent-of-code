use aoc_lib::answer;
use aoc_lib::reader::Reader;
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

    fn next(&self, start: usize) -> HashInfo {
        let mut i = start;
        loop {
            let mut digest = md5::compute(format!("{}{i}", self.prefix));
            let mut hash = [0; 32];
            for _ in 0..(self.n - 1) {
                Self::fill_hash(&mut hash, digest);
                digest = md5::compute(hash);
            }
            Self::fill_hash(&mut hash, digest);
            if let Some(&triple) = Self::repeats(&hash, 3).first() {
                return HashInfo {
                    i,
                    triple,
                    cinqs: Self::repeats(&hash, 5),
                };
            }
            i += 1;
        }
    }

    fn fill_hash(buffer: &mut [u8; 32], digest: md5::Digest) {
        for i in 0..16 {
            let ch = digest[i];
            let (v1, v2) = (ch >> 4, ch & 0b0000_1111);
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
    answer::part1(15168, generate(prefix.clone(), 1));
    answer::part2(20864, generate(prefix.clone(), 2_017));
}

fn generate(prefix: String, n: usize) -> usize {
    let hasher = Hasher::new(prefix, n);

    let mut hashes = VecDeque::new();
    hashes.push_back(hasher.next(0));

    let mut keys = Vec::new();
    while keys.len() < 64 {
        let hash = hashes.front().unwrap().clone();
        while hashes.back().unwrap().i < hash.i + 1_000 {
            hashes.push_back(hasher.next(hashes.back().unwrap().i + 1));
        }
        hashes.pop_front().unwrap();
        for other in hashes.iter() {
            if hash.i + 1000 < other.i {
                break;
            }
            if other.cinqs.contains(&hash.triple) {
                keys.push(hash.i);
                break;
            }
        }
    }
    keys[63]
}
