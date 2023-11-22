from aoc import answer
from aoc.computer import Computer
from aoc.parser import Parser


def main() -> None:
    answer.part1(198, run_until_success())


def run_until_success() -> int:
    i = 0
    while True:
        try:
            run_computer(i)
            return i
        except Exception:
            pass
        i += 1


def run_computer(initial_value: int):
    computer = Computer(registers=dict(a=initial_value, b=0, c=0, d=0), num_outputs=100)
    computer.run(Parser().lines())


if __name__ == "__main__":
    main()
