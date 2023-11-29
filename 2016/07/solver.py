from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class IpAddress:
    sequences: list[str]
    hyper_sequences: list[str]

    def ssl(self) -> bool:
        in_main, in_hyper = self.subsequences(3)
        for s1 in in_main:
            for s2 in in_hyper:
                if s1[0] == s2[1] and s1[1] == s2[0]:
                    return True
        return False

    def tls(self) -> bool:
        in_main, in_hyper = self.subsequences(4)
        return len(in_main) > 0 and len(in_hyper) == 0

    def subsequences(self, length: int) -> tuple[set[str], set[str]]:
        in_main = self.all_subsequences(self.sequences, length)
        in_hyper = self.all_subsequences(self.hyper_sequences, length)
        return in_main, in_hyper

    def all_subsequences(self, sequences: list[str], length: int) -> set[str]:
        results = [self.subsequence(sequence, length) for sequence in sequences]
        flattened = [value for values in results for value in values]
        return set(flattened)

    def subsequence(self, sequence: str, length: int) -> list[str]:
        result: list[str] = []
        for i in range(len(sequence) - length + 1):
            value = sequence[i : i + length]
            if value[0] == value[-1] and value[1] == value[-2] and value[0] != value[1]:
                result.append(value)
        return result


def main() -> None:
    ips = get_ip_addresses()
    answer.part1(118, sum([ip.tls() for ip in ips]))
    answer.part2(260, sum([ip.ssl() for ip in ips]))


def get_ip_addresses() -> list[IpAddress]:
    def parse_ip_address(line: str) -> IpAddress:
        parts: list[str] = line.split("[")
        sequences: list[str] = [parts[0]]
        hyper_sequences: list[str] = []
        for part in parts[1:]:
            hyper, regular = part.split("]")
            hyper_sequences.append(hyper)
            sequences.append(regular)
        return IpAddress(sequences, hyper_sequences)

    return [parse_ip_address(line) for line in Parser().lines()]


if __name__ == "__main__":
    main()
