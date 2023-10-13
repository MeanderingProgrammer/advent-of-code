from aoc import answer
from aoc.int_code import Computer
from aoc.parser import Parser


class Direction:
    def __init__(self):
        self.index = 0
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def rotate(self, value):
        self.index += value if value == 1 else -1

    def step(self, position):
        to_go = self.directions[self.index % len(self.directions)]
        return position[0] + to_go[0], position[1] + to_go[1]


class PaintBot:
    def __init__(self, memory, starting_color):
        self.computer = Computer(self)
        self.computer.set_memory(memory)

        self.color = True

        self.direction = Direction()
        self.grid = {}
        self.position = (0, 0)
        self.grid[self.position] = starting_color

    def run(self):
        self.computer.run()

    def get_input(self):
        return self.grid[self.position] if self.position in self.grid else 0

    def add_output(self, value):
        if self.color:
            self.grid[self.position] = value
        else:
            self.direction.rotate(value)
            self.position = self.direction.step(self.position)
        self.color = not self.color

    def get_grid(self):
        xs = [position[0] for position in self.grid]
        ys = [position[1] for position in self.grid]

        rows = []
        for y in range(min(ys), max(ys) + 1):
            row = []
            for x in range(max(xs), min(xs) - 1, -1):
                value = self.grid.get((x, y), 0)
                value = "." if value == 0 else "#"
                row.append(value)
            rows.append("".join(row))
        return "\n".join(rows)


def main():
    answer.part1(1909, len(run(0).grid))
    # Part 2: JUFEKHPH
    print("Part 2")
    print(run(1).get_grid())


def run(setting):
    bot = PaintBot(get_memory(), setting)
    bot.run()
    return bot


def get_memory():
    return Parser().int_csv()


if __name__ == "__main__":
    main()
