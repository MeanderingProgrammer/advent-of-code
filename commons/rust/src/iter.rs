use crate::collections::HashSet;
use std::fmt::{Display, Write};
use std::hash::Hash;

pub trait Iter: Iterator {
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

impl<T> Iter for T where T: Iterator + ?Sized {}
