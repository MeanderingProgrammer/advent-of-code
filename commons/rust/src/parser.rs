use crate::Iter;
use std::fmt::Debug;
use std::str::FromStr;

#[derive(Debug)]
pub struct Parser;

impl Parser {
    pub fn all<const N: usize, P>(s: &str, pat: P) -> Option<[&str; N]>
    where
        P: AsRef<str>,
    {
        Self::normalize(s, pat).into_iter().array()
    }

    pub fn values<const N: usize, P, T>(s: &str, pat: P) -> Option<[T; N]>
    where
        P: AsRef<str>,
        T: FromStr,
    {
        Self::normalize(s, pat)
            .into_iter()
            .flat_map(|s| s.parse())
            .array()
    }

    pub fn nth<const N: usize, P>(s: &str, pat: P, ns: [usize; N]) -> [&str; N]
    where
        P: AsRef<str>,
    {
        let parts = Self::normalize(s, pat);
        ns.map(|n| parts[n])
    }

    pub fn nth_rev<const N: usize, P>(s: &str, pat: P, ns: [usize; N]) -> [&str; N]
    where
        P: AsRef<str>,
    {
        let parts = Self::normalize(s, pat);
        ns.map(|n| parts[parts.len() - 1 - n])
    }

    pub fn enclosed(s: &str, open: char, close: char) -> Option<&str> {
        let (start, end) = (s.find(open)?, s.rfind(close)?);
        Some(&s[start + 1..end])
    }

    fn normalize<P>(s: &str, pat: P) -> Vec<&str>
    where
        P: AsRef<str>,
    {
        s.split(pat.as_ref())
            .map(|s| s.trim_matches([' ', '.', ',', '#']))
            .collect()
    }
}
