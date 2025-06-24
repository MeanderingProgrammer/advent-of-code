from typing import override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


class JumpDroid(Bus):
    def __init__(self, actions: list[str]):
        program: list[str] = []
        for action in actions:
            program.extend([value for value in action])
            program.append("\n")
        self.program: list[str] = program
        self.value: int | None = None

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        return ord(self.program.pop(0))

    @override
    def add_output(self, value: int) -> None:
        self.value = value


@answer.timer
def main() -> None:
    memory = Parser().int_csv()
    answer.part1(
        19357761,
        run_droid(
            memory,
            # If one ahead is missing always Jump
            "NOT A J",
            # If 3 ahead is missing
            "NOT C T",
            "OR T J",
            # If 2 ahead is missing
            "NOT B T",
            "OR T J",
            # Must always have thing 4 tiles ahead
            "AND D J",
            # Force T to False
            "NOT A T",
            "AND A T",
            # Start the script
            "WALK",
        ),
    )

    answer.part2(
        1142249706,
        run_droid(
            memory,
            # If one ahead is missing always Jump
            "NOT A J",
            # If 3 ahead is missing
            "NOT C T",
            "OR T J",
            # If 2 ahead is missing
            "NOT B T",
            "OR T J",
            # Must always have thing 4 tiles ahead
            "AND D J",
            # Force T to False
            "NOT A T",
            "AND A T",
            # If after we land is blank
            "OR E T",
            "OR H T",
            "AND T J",
            # Start the script
            "RUN",
        ),
    )


def run_droid(memory: list[int], *actions: str) -> int | None:
    droid = JumpDroid(list(actions))
    Computer(bus=droid, memory=memory.copy()).run()
    return droid.value


if __name__ == "__main__":
    main()
