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
    # Part 2: 5088037
    recursive = True
    modules = get_modules()
    fuel_needed = [module.fuel(recursive) for module in modules]
    print('Total fuel needed = {}'.format(sum(fuel_needed)))


def get_modules():
    with open('data.txt', 'r') as f:
        data = f.read()
    return [Module(datum) for datum in data.split('\n')]


if __name__ == '__main__':
    main()

