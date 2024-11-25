#[derive(Debug, Clone, Default, Hash, PartialEq, Eq)]
pub struct BitSet {
    values: u64,
}

impl BitSet {
    pub fn contains(&self, value: u8) -> bool {
        (self.values >> value) & 1 == 1
    }

    pub fn add(&mut self, value: u8) {
        self.values |= 1 << value;
    }

    pub fn values(&self) -> impl Iterator<Item = u8> + '_ {
        (0..64).filter(|&i| self.contains(i))
    }
}
