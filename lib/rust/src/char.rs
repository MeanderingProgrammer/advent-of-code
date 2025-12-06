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
            Some(Char::digit(ch))
        } else {
            Some(Char::lower_index(ch))
        }
    }
}

#[derive(Debug)]
pub struct Char;

impl Char {
    pub fn digit(ch: char) -> u8 {
        (ch as u8) - b'0'
    }

    pub fn lower_index(ch: char) -> u8 {
        (ch as u8) - b'a'
    }

    pub fn upper_index(ch: char) -> u8 {
        (ch as u8) - b'A'
    }

    pub fn lower_char(idx: u8) -> char {
        (idx + b'a') as char
    }
}
