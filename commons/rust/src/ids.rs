use crate::HashMap;
use std::cmp::Eq;
use std::hash::Hash;

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
