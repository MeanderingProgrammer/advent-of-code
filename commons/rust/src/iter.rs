use crate::collections::{HashMap, HashSet};
use std::fmt::{Display, Write};
use std::hash::Hash;

// Extra methods for Iterators based largely off of the Itertools crate
pub trait Iter: Iterator {
    fn vec(self) -> Vec<Self::Item>
    where
        Self: Sized,
    {
        self.collect()
    }

    fn sorted(self) -> std::vec::IntoIter<Self::Item>
    where
        Self: Sized,
        Self::Item: Ord,
    {
        let mut values = self.vec();
        values.sort();
        values.into_iter()
    }

    fn counts(self) -> HashMap<Self::Item, usize>
    where
        Self: Sized,
        Self::Item: Eq + Hash,
    {
        let mut counts = HashMap::default();
        self.for_each(|value| *counts.entry(value).or_default() += 1);
        counts
    }

    fn combinations(self, k: usize) -> Product<Self::Item>
    where
        Self: Sized,
        Self::Item: Clone,
    {
        Product::new(self.vec(), k, ProductKind::Combination)
    }

    fn permutations(self) -> Product<Self::Item>
    where
        Self: Sized,
        Self::Item: Clone,
    {
        let values = self.vec();
        let k = values.len();
        Product::new(values, k, ProductKind::Permutation)
    }

    fn unique(&mut self) -> usize
    where
        Self::Item: Hash + Eq,
    {
        self.collect::<HashSet<_>>().len()
    }

    fn join(&mut self, sep: &str) -> String
    where
        Self::Item: Display,
    {
        match self.next() {
            None => String::default(),
            Some(first) => {
                let mut result = String::default();
                write!(&mut result, "{}", first).unwrap();
                self.for_each(|value| {
                    result.push_str(sep);
                    write!(&mut result, "{}", value).unwrap();
                });
                result
            }
        }
    }

    fn minmax(&mut self) -> Option<(Self::Item, Self::Item)>
    where
        Self::Item: Clone + PartialOrd,
    {
        match self.next() {
            None => None,
            Some(first) => {
                let (mut min, mut max) = (first.clone(), first);
                self.for_each(|value| {
                    if value < min {
                        min = value;
                    } else if value > max {
                        max = value;
                    }
                });
                Some((min, max))
            }
        }
    }
}

#[derive(Debug)]
enum ProductKind {
    Combination,
    Permutation,
}

#[derive(Debug)]
pub struct Product<T> {
    values: Vec<T>,
    indices: Vec<usize>,
    kind: ProductKind,
    done: bool,
}

impl<T> Product<T> {
    fn new(values: Vec<T>, k: usize, kind: ProductKind) -> Self {
        assert!(k <= values.len());
        Self {
            values,
            indices: (0..k).collect(),
            kind,
            done: false,
        }
    }

    fn next_combination(&mut self) -> bool {
        let (n, k) = (self.values.len(), self.indices.len());
        let mut i = k;
        while i > 0 {
            i -= 1;
            if self.indices[i] != i + n - k {
                break;
            }
        }
        if self.indices[i] == i + n - k {
            true
        } else {
            self.indices[i] += 1;
            for j in i + 1..k {
                self.indices[j] = self.indices[j - 1] + 1;
            }
            false
        }
    }

    fn next_permutation(&mut self) -> bool {
        let (n, k) = (self.values.len(), self.indices.len());
        assert_eq!(n, k);
        let mut i = k - 2;
        while self.indices[i] >= self.indices[i + 1] {
            if i == 0 {
                return true;
            }
            i -= 1;
        }
        let mut j = k - 1;
        while self.indices[i] >= self.indices[j] {
            j -= 1;
        }
        self.indices.swap(i, j);
        self.indices[i + 1..].reverse();
        false
    }
}

impl<T: Clone> Iterator for Product<T> {
    type Item = Vec<T>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.done {
            None
        } else {
            let result = self
                .indices
                .iter()
                .map(|i| self.values[*i].clone())
                .collect();
            self.done = match self.kind {
                ProductKind::Combination => self.next_combination(),
                ProductKind::Permutation => self.next_permutation(),
            };
            Some(result)
        }
    }
}

impl<T> Iter for T where T: Iterator + ?Sized {}
