import commons.answer as answer
from commons.aoc_parser import Parser


class Number:

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self, prefer_addition):
        return self.value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}'.format(self.value)


class Expression:

    def __init__(self, expression):
        self.expressions = []
        self.operators = []

        i = 0
        while i < len(expression):
            char = expression[i]
            if char == '(':
                end_index = self.get_end_index(i, expression)
                self.expressions.append(Expression(expression[i+1:end_index]))
                i = end_index + 1
            elif char.isdigit():
                self.expressions.append(Number(char))
                i += 1
            else:
                self.operators.append(char)
                i += 1

    def evaluate(self, prefer_addition):
        if len(self.expressions) == 1:
            return self.expressions[0].evaluate(prefer_addition)

        if prefer_addition:
            operator = '+' if '+' in self.operators else '*'
            index = self.operators.index(operator)
        else:
            operator = self.operators[0]
            index = 0
        
        left = self.expressions[index]
        right = self.expressions[index+1]
        
        if operator == '+':
            result = left.evaluate(prefer_addition) + right.evaluate(prefer_addition)
        else:
            result = left.evaluate(prefer_addition) * right.evaluate(prefer_addition)

        self.expressions[index] = Number(result)
        del self.expressions[index+1]
        del self.operators[index]

        return self.evaluate(prefer_addition)

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = '(' + str(self.expressions[0])
        for i in range(len(self.operators)):
            result += str(self.operators[i])
            result += str(self.expressions[i+1])
        return result + ')'

    @staticmethod
    def get_end_index(start_index, expression):
        count = 0
        for i in range(start_index, len(expression)):
            letter = expression[i]
            if letter == '(':
                count += 1
            elif letter == ')':
                count -= 1
                if count == 0:
                    return i


def main():
    answer.part1(69490582260, sum_expressions(False))
    answer.part2(362464596624526, sum_expressions(True))


def sum_expressions(prefer_addition):
    expressions = get_expressions()
    answers = [expression.evaluate(prefer_addition) for expression in expressions]
    return sum(answers)


def get_expressions():
    return [Expression(line.replace(' ', '')) for line in Parser().lines()]


if __name__ == '__main__':
    main()
