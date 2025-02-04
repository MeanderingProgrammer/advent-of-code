pub trait FromChar: Sized {
    fn from_char(ch: char) -> Option<Self>;
}

impl FromChar for char {
    fn from_char(ch: char) -> Option<Self> {
        Some(ch)
    }
}

impl FromChar for u8 {
    fn from_char(ch: char) -> Option<Self> {
        if ch.is_ascii_digit() {
            Some(Convert::idx_int(ch))
        } else {
            Some(Convert::idx_lower(ch))
        }
    }
}

#[derive(Debug)]
pub struct Convert;

impl Convert {
    pub fn idx_int(ch: char) -> u8 {
        (ch as u8) - b'0'
    }

    pub fn idx_lower(ch: char) -> u8 {
        (ch as u8) - b'a'
    }

    pub fn idx_upper(ch: char) -> u8 {
        (ch as u8) - b'A'
    }

    pub fn char_lower(idx: u8) -> char {
        (idx + b'a') as char
    }

    pub fn ch(s: &str) -> char {
        s.chars().next().unwrap()
    }

    pub fn idx_lower_str(s: &str) -> u32 {
        s.to_lowercase()
            .char_indices()
            .map(|(i, ch)| 26u32.pow(i as u32) * (Self::idx_lower(ch) as u32))
            .sum()
    }
}
