use std::{collections, hash};

pub type HashMap<K, V> = collections::HashMap<K, V, BuildHasher>;
pub type HashSet<V> = collections::HashSet<V, BuildHasher>;
pub type BuildHasher = hash::BuildHasherDefault<Hasher>;

// Simplified implementation of: https://github.com/rust-lang/rustc-hash
#[derive(Debug, Default)]
pub struct Hasher {
    hash: u64,
}

impl hash::Hasher for Hasher {
    #[inline]
    fn finish(&self) -> u64 {
        self.hash.rotate_left(26)
    }

    #[inline]
    fn write(&mut self, bytes: &[u8]) {
        let mut s0 = 0x243f6a8885a308d3;
        let mut s1 = 0x13198a2e03707344;
        let len = bytes.len();
        match len {
            0 => {}
            1..=3 => {
                let lo = bytes[0] as u64;
                let mid = bytes[len / 2] as u64;
                let hi = bytes[len - 1] as u64;
                s0 ^= lo;
                s1 ^= (hi << 8) | mid;
            }
            4..=7 => {
                s0 ^= Self::read_u32(&bytes[0..4]) as u64;
                s1 ^= Self::read_u32(&bytes[len - 4..]) as u64;
            }
            8..=16 => {
                s0 ^= Self::read_u64(&bytes[0..8]);
                s1 ^= Self::read_u64(&bytes[len - 8..]);
            }
            _ => {
                let chunks = bytes.chunks_exact(16);
                for chunk in chunks {
                    let x = Self::read_u64(&chunk[0..8]);
                    let y = Self::read_u64(&chunk[8..]);
                    let t = Self::mix(s0 ^ x, 0xa4093822299f31d0 ^ y);
                    s0 = s1;
                    s1 = t;
                }
                let suffix = &bytes[len - 16..];
                s0 ^= Self::read_u64(&suffix[0..8]);
                s1 ^= Self::read_u64(&suffix[8..]);
            }
        }
        let i = Self::mix(s0, s1) ^ (len as u64);
        self.add(i);
    }

    #[inline]
    fn write_u8(&mut self, i: u8) {
        self.add(i as u64);
    }

    #[inline]
    fn write_u16(&mut self, i: u16) {
        self.add(i as u64);
    }

    #[inline]
    fn write_u32(&mut self, i: u32) {
        self.add(i as u64);
    }

    #[inline]
    fn write_u64(&mut self, i: u64) {
        self.add(i);
    }

    #[inline]
    fn write_u128(&mut self, i: u128) {
        self.add(i as u64);
        self.add((i >> 64) as u64);
    }

    #[inline]
    fn write_usize(&mut self, i: usize) {
        self.add(i as u64);
    }
}

impl Hasher {
    #[inline]
    fn add(&mut self, i: u64) {
        self.hash = self.hash.wrapping_add(i).wrapping_mul(0xf1357aea2e62a9c5);
    }

    #[inline]
    fn read_u32(bytes: &[u8]) -> u32 {
        u32::from_le_bytes(bytes.try_into().unwrap())
    }

    #[inline]
    fn read_u64(bytes: &[u8]) -> u64 {
        u64::from_le_bytes(bytes.try_into().unwrap())
    }

    #[inline]
    fn mix(x: u64, y: u64) -> u64 {
        let full = (x as u128).wrapping_mul(y as u128);
        let lo = full as u64;
        let hi = (full >> 64) as u64;
        lo ^ hi
    }
}
