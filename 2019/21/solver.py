from typing import Optional, override

from aoc import answer
from aoc.int_code import Bus, Computer
from aoc.parser import Parser


class JumpDroid(Bus):
    def __init__(self, actual_program: list[str]):
        self.program = self.__transform(actual_program)
        self.buffer = ""
        self.value = None

    @override
    def active(self) -> bool:
        return True

    @override
    def get_input(self) -> int:
        self.buffer = ""
        value = self.program.pop(0)
        return ord(value)

    @override
    def add_output(self, value: int) -> None:
        if value < 256:
            self.buffer += chr(value)
        else:
            self.value = value

    @staticmethod
    def __transform(actual_program: list[str]) -> list[str]:
        program: list[str] = []
        for instruction in actual_program:
            real = [value for value in instruction]
            real.append("\n")
            program.extend(real)
        return program


@answer.timer
def main() -> None:
    answer.part1(
        19357761,
        run_droid(
            [
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
            ]
        ),
    )

    answer.part2(
        1142249706,
        run_droid(
            [
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
            ]
        ),
    )


def run_droid(actual_program) -> Optional[int]:
    droid = JumpDroid(actual_program)
    Computer(bus=droid, memory=Parser().int_csv()).run()
    return droid.value


if __name__ == "__main__":
    main()
