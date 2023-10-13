import itertools
from aoc import answer
from aoc.parser import Parser


def main():
    weights = Parser().int_lines()
    answer.part1(10439961859, store_weights(weights, 3))
    answer.part2(72050269, store_weights(weights, 4))


def store_weights(weights, sections):
    total_weight = sum(weights)
    per_compartment = total_weight // sections

    options = []
    for option in group(weights, per_compartment, sections):
        first_group = option[0]
        if len(options) > 0 and len(first_group) > len(options[0]):
            break
        options.append(first_group)
    return get_lowest_entaglement(options)


def group(weights, per_compartment, compartments):
    for total_packages in range(1, len(weights) + 1):
        for sub_weights in itertools.combinations(weights, total_packages):
            if sum(sub_weights) == per_compartment:
                if compartments == 1:
                    yield [sub_weights]
                else:
                    for sub_group in group(
                        remove(weights, sub_weights), per_compartment, compartments - 1
                    ):
                        yield [sub_weights] + sub_group
                        # No need to search for multiple matches that start with the current
                        # sub group, simply continue to next group
                        break


def remove(data, ignore):
    return [datum for datum in data if datum not in ignore]


def get_lowest_entaglement(options):
    entaglements = [get_entaglement(option) for option in options]
    return min(entaglements)


def get_entaglement(values):
    result = 1
    for value in values:
        result *= value
    return result


if __name__ == "__main__":
    main()
