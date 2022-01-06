import commons.answer as answer
from commons.aoc_parser import Parser


class IpAddress:

    def __init__(self, value):
        values = value.split('[')

        self.sequences = [values[0]]
        self.hyper_sequences = []

        for value in values[1:]:
            value = value.split(']')
            self.hyper_sequences.append(value[0])
            self.sequences.append(value[1])

    def ssl(self):
        in_main, in_hyper = self.subsequences(3)
        for s1 in in_main:
            for s2 in in_hyper:
                if self.inverses(s1, s2):
                    return True
        return False

    def tls(self):
        in_main, in_hyper = self.subsequences(4)
        return len(in_main) > 0 and len(in_hyper) == 0

    def subsequences(self, length):
        in_main = [self.subsequence(sequence, length) for sequence in self.sequences]
        in_main = [value for values in in_main for value in values]

        in_hyper = [self.subsequence(sequence, length) for sequence in self.hyper_sequences]
        in_hyper = [value for values in in_hyper for value in values]

        return set(in_main), set(in_hyper)

    def subsequence(self, sequence, length):
        result = []
        for i in range(len(sequence)-length+1):
            value = sequence[i:i+length]
            if self.palindrome(value):
                result.append(value)
        return result

    @staticmethod
    def palindrome(value):
        conditions = [
            value[0] == value[-1],
            value[1] == value[-2],
            value[0] != value[1]
        ]
        return all(conditions)

    @staticmethod
    def inverses(s1, s2):
        conditions = [
            s1[0] == s2[1],
            s1[1] == s2[0]
        ]
        return all(conditions)


def main():
    ip_addresses = get_ip_addresses()
    
    supported = [ip_address.tls() for ip_address in ip_addresses]
    answer.part1(118, sum(supported))
    
    supported = [ip_address.ssl() for ip_address in ip_addresses]
    answer.part2(260, sum(supported))


def get_ip_addresses():
    return [IpAddress(line) for line in Parser().lines()]


if __name__ == '__main__':
    main()
