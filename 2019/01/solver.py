from dataclasses import dataclass

from aoc import answer
from aoc.parser import Parser


@dataclass(frozen=True)
class Module:
    mass: int

    def fuel(self, recursive: bool) -> int:
        fuel = (self.mass // 3) - 2
        if not recursive:
            return fuel
        else:
            return fuel + Module(fuel).fuel(True) if fuel > 0 else 0


@answer.timer
def main() -> None:
    modules = [Module(mass) for mass in Parser().int_lines()]
    answer.part1(3393938, get_fuel(modules, False))
    answer.part2(5088037, get_fuel(modules, True))


def get_fuel(modules: list[Module], recursive: bool) -> int:
    return sum([module.fuel(recursive) for module in modules])


if __name__ == "__main__":
    main()
