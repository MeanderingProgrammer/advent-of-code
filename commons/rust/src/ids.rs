use crate::HashMap;
use std::cmp::Eq;
use std::hash::Hash;

#[derive(Debug)]
pub struct Base {}

impl Base {
    pub fn str_insensitive(s: &str) -> u32 {
        s.to_lowercase()
            .char_indices()
            .map(|(i, ch)| 26u32.pow(i as u32) * (Self::ch_lower(ch) as u32))
            .sum()
    }

    pub fn ch_lower(ch: char) -> u8 {
        (ch as u8) - b'a'
    }

    pub fn ch_upper(ch: char) -> u8 {
        (ch as u8) - b'A'
    }
}

#[derive(Debug, Default)]
pub struct Ids<K> {
    values: HashMap<K, usize>,
}

impl<K> Ids<K>
where
    K: Clone + Hash + Eq,
{
    pub fn set(&mut self, key: &K) -> usize {
        let n = self.values.len();
        *self.values.entry(key.clone()).or_insert(n)
    }

    pub fn get(&self, key: &K) -> usize {
        *self.values.get(key).unwrap()
    }
}
