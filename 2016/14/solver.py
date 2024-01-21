import hashlib
from collections import deque
from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class HashInfo:
    value: str
    cinqs: list[str]


@answer.timer
def main() -> None:
    prefix = Parser().string()
    answer.part1(15168, generate(prefix, 1))
    answer.part2(20864, generate(prefix, 2_017))


def generate(prefix: str, num_hashes: int) -> int:
    i = 0
    hash_infos = deque()
    while i < 1_000:
        hash_infos.append(get_hash(prefix, i, num_hashes))
        i += 1
    keys = []
    while len(keys) < 64:
        hash_info = hash_infos.popleft()
        hash_infos.append(get_hash(prefix, i, num_hashes))
        triples = get_repeats(hash_info.value, 3)
        if len(triples) > 0:
            if contains(hash_infos, triples[0]):
                keys.append(i - len(hash_infos))
        i += 1
    return keys[-1]


def get_hash(prefix: str, index: int, n: int) -> HashInfo:
    value = prefix + str(index)
    for _ in range(n):
        value = hashlib.md5(str.encode(value)).hexdigest()
    return HashInfo(value=value, cinqs=get_repeats(value, 5))


def get_repeats(hashed: str, length: int) -> list[str]:
    repeats = []
    for i in range(len(hashed) - length + 1):
        value = hashed[i : i + length]
        if len(set([v for v in value])) == 1:
            repeats.append(value[0])
    return repeats


def contains(hash_infos: deque[HashInfo], value: str) -> bool:
    for hash_info in hash_infos:
        if value in hash_info.cinqs:
            return True
    return False


if __name__ == "__main__":
    main()
