import re


def in_range(value, minimum, maximum):
    return value >= minimum and value <= maximum


def birth_year(value):
    value = int(value)
    return in_range(value, 1920, 2002)


def issue_year(value):
    value = int(value)
    return in_range(value, 2010, 2020)


def experation_year(value):
    value = int(value)
    return in_range(value, 2020, 2030)


def height(value):
    height = int(value[:-2])
    unit = value[-2:]
    if unit == 'cm':
        return in_range(height, 150, 193)
    elif unit == 'in':
        return in_range(height, 59, 76)
    else:
        return False


def hair_color(value):
    expression = '^#[0-9,a-f]{6}$'
    match = re.search(expression, value)
    return match is not None


def eye_color(value):
    valid = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    return value in valid


def passport_id(value):
    expression = '^[0-9]{9}$'
    match = re.search(expression, value)
    return match is not None


FIELD_VALIDATORS = {
    'byr': birth_year,
    'iyr': issue_year,
    'eyr': experation_year,
    'hgt': height,
    'hcl': hair_color,
    'ecl': eye_color,
    'pid': passport_id
}


class Passport:

    def __init__(self):
        self.data = {}

    def add(self, line):
        parts = line.split()
        for part in parts:
            kv = part.split(':')
            self.data[kv[0]] = kv[1]

    def validate(self):
        for field in FIELD_VALIDATORS:
            if field not in self.data:
                return False
            validator = FIELD_VALIDATORS[field]
            value = self.data[field]
            if not validator(value):
                return False
        return True


def main():
    passports = process()
    
    num_valid = 0
    for passport in passports:
        is_valid = passport.validate()
        if is_valid:
            num_valid += 1
    print('Total invalid = {}'.format(num_valid))


def process():
    data = []
    f = open('data.txt', 'r')

    passport = Passport()
    for line in f:
        line = line.strip()
        if len(line) == 0:
            data.append(passport)
            passport = Passport()
        else:
            passport.add(line)

    data.append(passport)
    f.close()
    return data


if __name__ == '__main__':
    main()

