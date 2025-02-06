use crate::Char;
use std::fmt::Debug;
use std::str::FromStr;

#[derive(Debug)]
pub struct Str;

impl Str {
    pub fn is_upper(s: &str) -> bool {
        s.chars().all(|ch| ch.is_uppercase())
    }

    pub fn first(s: &str) -> char {
        s.chars().next().unwrap()
    }

    pub fn lower_index(s: &str) -> u32 {
        s.to_lowercase()
            .char_indices()
            .map(|(i, ch)| 26u32.pow(i as u32) * (Char::lower_index(ch) as u32))
            .sum()
    }

    pub fn nth<T>(s: &str, pat: char, n: usize) -> T
    where
        T: FromStr,
        T::Err: Debug,
    {
        let value = s.split(pat).nth(n).unwrap();
        value.trim().parse().unwrap()
    }

    pub fn nth_rev<T>(s: &str, pat: char, n: usize) -> T
    where
        T: FromStr,
        T::Err: Debug,
    {
        let values = s.split(pat).collect::<Vec<_>>();
        let value = values[values.len() - 1 - n];
        value.trim().parse().unwrap()
    }

    pub fn enclosed(s: &str, open: char, close: char) -> Option<&str> {
        let (start, end) = (s.find(open)?, s.rfind(close)?);
        Some(&s[start + 1..end])
    }
}
