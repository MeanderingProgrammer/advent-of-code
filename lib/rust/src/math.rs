pub fn lcm(values: Vec<usize>) -> usize {
    let mut current = values[0];
    for value in values.iter().skip(1) {
        current = lcm_pair(current, *value);
    }
    current
}

pub fn lcm_pair(a: usize, b: usize) -> usize {
    a * b / gcd(a, b)
}

pub fn gcd(a: usize, b: usize) -> usize {
    if b == 0 {
        return a;
    }
    gcd(b, a % b)
}
