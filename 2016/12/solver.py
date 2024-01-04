from aoc import answer
from aoc.computer import Computer
from aoc.parser import Parser


@answer.timer
def main() -> None:
    answer.part1(318117, run(0))
    answer.part2(9227771, run(1))


def run(c_value: int) -> int:
    computer = Computer(registers=dict(a=0, b=0, c=c_value, d=0))
    computer.run(Parser().lines())
    return computer.get("a")


if __name__ == "__main__":
    main()
