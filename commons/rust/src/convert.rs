pub fn char_index(ch: char) -> u8 {
    (ch.to_ascii_lowercase() as u8) - b'a'
}
