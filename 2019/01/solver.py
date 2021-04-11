from commons.aoc_parser import Parser


class Module:

    def __init__(self, value):
        self.mass = int(value)
    
    def fuel(self, recursive):
        fuel = (self.mass // 3) - 2
        if not recursive:
            return fuel
        else:
            return fuel + Module(fuel).fuel(True) if fuel > 0 else 0


def main():
    # Part 1: 3393938
    print('Part 1: {}'.format(get_fuel(False)))
    # Part 2: 5088037
    print('Part 2: {}'.format(get_fuel(True)))


def get_fuel(recursive):
    modules = get_modules()
    fuel_needed = [module.fuel(recursive) for module in modules]
    return sum(fuel_needed)


def get_modules():
    return [Module(line) for line in Parser().lines()]


if __name__ == '__main__':
    main()
