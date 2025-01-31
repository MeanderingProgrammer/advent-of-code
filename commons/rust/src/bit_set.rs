#[derive(Debug, Clone, Default, Hash, PartialEq, Eq)]
pub struct BitSet {
    values: u64,
}

impl<const N: usize> From<[u8; N]> for BitSet {
    fn from(values: [u8; N]) -> Self {
        BitSet::default().with_extend(values)
    }
}

impl BitSet {
    pub fn add(&mut self, value: u8) {
        self.values |= 1 << value;
    }

    pub fn extend<const N: usize>(&mut self, values: [u8; N]) {
        values.into_iter().for_each(|value| self.add(value));
    }

    pub fn with_extend<const N: usize>(&self, values: [u8; N]) -> Self {
        let mut result = self.clone();
        result.extend(values);
        result
    }

    pub fn contains(&self, value: u8) -> bool {
        (self.values >> value) & 1 == 1
    }

    pub fn values(&self) -> impl Iterator<Item = u8> + '_ {
        (0..64).filter(|&i| self.contains(i))
    }
}
