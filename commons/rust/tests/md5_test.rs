use aoc::Md5;

#[test]
fn test_compute() {
    let input = "The quick brown fox jumps over the lazy dog";
    let inputs = std::array::from_fn(|_| input.to_string());
    #[rustfmt::skip]
    let expected = [
        0x9e, 0x10, 0x7d, 0x9d, 0x37, 0x2b, 0xb6, 0x82,
        0x6b, 0xd8, 0x1d, 0x35, 0x42, 0xa4, 0x19, 0xd6,
    ];
    assert_eq!([expected; 8], Md5::from(inputs).compute());
}
