use wide::u32x8;

#[derive(Debug)]
pub struct Md5 {
    pub buffers: [[u8; 64]; 8],
}

impl From<[String; 8]> for Md5 {
    fn from(values: [String; 8]) -> Self {
        let buffers = values.map(|value| {
            let len = value.len();
            assert!(len < 56);
            let mut buffer = [0; 64];
            for (i, byte) in value.into_bytes().iter().enumerate() {
                buffer[i] = *byte;
            }
            buffer[len] = 0x80;
            let bits = (len as u64) * 8;
            buffer[56..64].copy_from_slice(&bits.to_le_bytes());
            buffer
        });
        Self::new(buffers)
    }
}

impl From<[[u32; 4]; 8]> for Md5 {
    fn from(values: [[u32; 4]; 8]) -> Self {
        fn hex_ascii(ch: u8) -> u8 {
            ch + if ch < 10 { 48 } else { 87 }
        }
        let buffers = values.map(|digest| {
            let mut buffer = [0; 64];
            for i in 0..digest.len() {
                let block = digest[i];
                buffer[i * 8] = hex_ascii(((block & 0xf0000000) >> 28) as u8);
                buffer[i * 8 + 1] = hex_ascii(((block & 0x0f000000) >> 24) as u8);
                buffer[i * 8 + 2] = hex_ascii(((block & 0x00f00000) >> 20) as u8);
                buffer[i * 8 + 3] = hex_ascii(((block & 0x000f0000) >> 16) as u8);
                buffer[i * 8 + 4] = hex_ascii(((block & 0x0000f000) >> 12) as u8);
                buffer[i * 8 + 5] = hex_ascii(((block & 0x00000f00) >> 8) as u8);
                buffer[i * 8 + 6] = hex_ascii(((block & 0x000000f0) >> 4) as u8);
                buffer[i * 8 + 7] = hex_ascii((block & 0x0000000f) as u8);
            }
            buffer[32] = 0x80;
            // 32 byte digest -> 256 bits -> [0, 1, 0, 0, 0, 0, 0, 0]
            buffer[57] = 1;
            buffer
        });
        Self::new(buffers)
    }
}

impl Md5 {
    pub fn new(buffers: [[u8; 64]; 8]) -> Self {
        Self { buffers }
    }

    pub fn compute(&self) -> [[u32; 4]; 8] {
        // https://en.wikipedia.org/wiki/MD5
        let (a, b, c, d) = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476);

        let m: [u32x8; 16] = std::array::from_fn(|i| {
            let buffers: [u32; 8] = std::array::from_fn(|j| {
                let byte: [u8; 4] = std::array::from_fn(|k| self.buffers[j][i * 4 + k]);
                u32::from_le_bytes(byte)
            });
            u32x8::new(buffers)
        });

        let [a, b, c, d] = Self::transform([a, b, c, d], m);

        std::array::from_fn(|i| [a[i], b[i], c[i], d[i]].map(|section| section.swap_bytes()))
    }

    fn transform(state: [u32; 4], m: [u32x8; 16]) -> [[u32; 8]; 4] {
        let mut a = u32x8::splat(state[0]);
        let mut b = u32x8::splat(state[1]);
        let mut c = u32x8::splat(state[2]);
        let mut d = u32x8::splat(state[3]);

        let (s1, s2, s3, s4) = (7, 12, 17, 22);
        a = Self::step::<1>([a, b, c, d], s1, 0xd76aa478, m[0]);
        d = Self::step::<1>([d, a, b, c], s2, 0xe8c7b756, m[1]);
        c = Self::step::<1>([c, d, a, b], s3, 0x242070db, m[2]);
        b = Self::step::<1>([b, c, d, a], s4, 0xc1bdceee, m[3]);
        a = Self::step::<1>([a, b, c, d], s1, 0xf57c0faf, m[4]);
        d = Self::step::<1>([d, a, b, c], s2, 0x4787c62a, m[5]);
        c = Self::step::<1>([c, d, a, b], s3, 0xa8304613, m[6]);
        b = Self::step::<1>([b, c, d, a], s4, 0xfd469501, m[7]);
        a = Self::step::<1>([a, b, c, d], s1, 0x698098d8, m[8]);
        d = Self::step::<1>([d, a, b, c], s2, 0x8b44f7af, m[9]);
        c = Self::step::<1>([c, d, a, b], s3, 0xffff5bb1, m[10]);
        b = Self::step::<1>([b, c, d, a], s4, 0x895cd7be, m[11]);
        a = Self::step::<1>([a, b, c, d], s1, 0x6b901122, m[12]);
        d = Self::step::<1>([d, a, b, c], s2, 0xfd987193, m[13]);
        c = Self::step::<1>([c, d, a, b], s3, 0xa679438e, m[14]);
        b = Self::step::<1>([b, c, d, a], s4, 0x49b40821, m[15]);

        let (s1, s2, s3, s4) = (5, 9, 14, 20);
        a = Self::step::<2>([a, b, c, d], s1, 0xf61e2562, m[1]);
        d = Self::step::<2>([d, a, b, c], s2, 0xc040b340, m[6]);
        c = Self::step::<2>([c, d, a, b], s3, 0x265e5a51, m[11]);
        b = Self::step::<2>([b, c, d, a], s4, 0xe9b6c7aa, m[0]);
        a = Self::step::<2>([a, b, c, d], s1, 0xd62f105d, m[5]);
        d = Self::step::<2>([d, a, b, c], s2, 0x02441453, m[10]);
        c = Self::step::<2>([c, d, a, b], s3, 0xd8a1e681, m[15]);
        b = Self::step::<2>([b, c, d, a], s4, 0xe7d3fbc8, m[4]);
        a = Self::step::<2>([a, b, c, d], s1, 0x21e1cde6, m[9]);
        d = Self::step::<2>([d, a, b, c], s2, 0xc33707d6, m[14]);
        c = Self::step::<2>([c, d, a, b], s3, 0xf4d50d87, m[3]);
        b = Self::step::<2>([b, c, d, a], s4, 0x455a14ed, m[8]);
        a = Self::step::<2>([a, b, c, d], s1, 0xa9e3e905, m[13]);
        d = Self::step::<2>([d, a, b, c], s2, 0xfcefa3f8, m[2]);
        c = Self::step::<2>([c, d, a, b], s3, 0x676f02d9, m[7]);
        b = Self::step::<2>([b, c, d, a], s4, 0x8d2a4c8a, m[12]);

        let (s1, s2, s3, s4) = (4, 11, 16, 23);
        a = Self::step::<3>([a, b, c, d], s1, 0xfffa3942, m[5]);
        d = Self::step::<3>([d, a, b, c], s2, 0x8771f681, m[8]);
        c = Self::step::<3>([c, d, a, b], s3, 0x6d9d6122, m[11]);
        b = Self::step::<3>([b, c, d, a], s4, 0xfde5380c, m[14]);
        a = Self::step::<3>([a, b, c, d], s1, 0xa4beea44, m[1]);
        d = Self::step::<3>([d, a, b, c], s2, 0x4bdecfa9, m[4]);
        c = Self::step::<3>([c, d, a, b], s3, 0xf6bb4b60, m[7]);
        b = Self::step::<3>([b, c, d, a], s4, 0xbebfbc70, m[10]);
        a = Self::step::<3>([a, b, c, d], s1, 0x289b7ec6, m[13]);
        d = Self::step::<3>([d, a, b, c], s2, 0xeaa127fa, m[0]);
        c = Self::step::<3>([c, d, a, b], s3, 0xd4ef3085, m[3]);
        b = Self::step::<3>([b, c, d, a], s4, 0x04881d05, m[6]);
        a = Self::step::<3>([a, b, c, d], s1, 0xd9d4d039, m[9]);
        d = Self::step::<3>([d, a, b, c], s2, 0xe6db99e5, m[12]);
        c = Self::step::<3>([c, d, a, b], s3, 0x1fa27cf8, m[15]);
        b = Self::step::<3>([b, c, d, a], s4, 0xc4ac5665, m[2]);

        let (s1, s2, s3, s4) = (6, 10, 15, 21);
        a = Self::step::<4>([a, b, c, d], s1, 0xf4292244, m[0]);
        d = Self::step::<4>([d, a, b, c], s2, 0x432aff97, m[7]);
        c = Self::step::<4>([c, d, a, b], s3, 0xab9423a7, m[14]);
        b = Self::step::<4>([b, c, d, a], s4, 0xfc93a039, m[5]);
        a = Self::step::<4>([a, b, c, d], s1, 0x655b59c3, m[12]);
        d = Self::step::<4>([d, a, b, c], s2, 0x8f0ccc92, m[3]);
        c = Self::step::<4>([c, d, a, b], s3, 0xffeff47d, m[10]);
        b = Self::step::<4>([b, c, d, a], s4, 0x85845dd1, m[1]);
        a = Self::step::<4>([a, b, c, d], s1, 0x6fa87e4f, m[8]);
        d = Self::step::<4>([d, a, b, c], s2, 0xfe2ce6e0, m[15]);
        c = Self::step::<4>([c, d, a, b], s3, 0xa3014314, m[6]);
        b = Self::step::<4>([b, c, d, a], s4, 0x4e0811a1, m[13]);
        a = Self::step::<4>([a, b, c, d], s1, 0xf7537e82, m[4]);
        d = Self::step::<4>([d, a, b, c], s2, 0xbd3af235, m[11]);
        c = Self::step::<4>([c, d, a, b], s3, 0x2ad7d2bb, m[2]);
        b = Self::step::<4>([b, c, d, a], s4, 0xeb86d391, m[9]);

        [
            (u32x8::splat(state[0]) + a).to_array(),
            (u32x8::splat(state[1]) + b).to_array(),
            (u32x8::splat(state[2]) + c).to_array(),
            (u32x8::splat(state[3]) + d).to_array(),
        ]
    }

    fn step<const N: u8>(state: [u32x8; 4], s: u32, k: u32, m: u32x8) -> u32x8 {
        let [a, b, c, d] = state;
        let f = match N {
            1 => (b & c) | (!b & d),
            2 => (b & d) | (c & !d),
            3 => b ^ c ^ d,
            4 => c ^ (b | !d),
            _ => unreachable!(),
        };
        let result = f + a + u32x8::splat(k) + m;
        let result = (result << s) | (result >> (32 - s));
        result + b
    }
}
