use aoc::Md5;

#[test]
fn test_compute() {
    let input = "The quick brown fox jumps over the lazy dog";
    let inputs = std::array::from_fn(|_| input.to_string());
    let expected = [0x9e107d9d, 0x372bb682, 0x6bd81d35, 0x42a419d6];
    assert_eq!([expected; 8], Md5::from(inputs).compute());
}
