from aoc import answer
from aoc.board import Grid, Point
from aoc.parser import Parser
from operator import attrgetter


class Character:
    def __init__(self, symbol, position, attack):
        self.symbol = symbol
        self.position = position
        self.hp = 200
        self.attack = attack

    def attacked(self, character):
        self.hp -= character.attack

    def alive(self):
        return self.hp > 0

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, o):
        return self.position < o.position

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{} HP = {} @ {}".format(self.symbol, self.hp, self.position)


class Game:
    def __init__(self, grid, goblins, elves):
        self.grid = grid
        self.goblins = goblins
        self.elves = elves
        self.round_num = 0
        self.num_elves = len(self.elves)

    def play(self):
        while True:
            if not self.make_move():
                break
            self.round_num += 1
        return self.get_result()

    def play_until_elf_dies(self):
        while True:
            if not self.make_move():
                break
            if len(self.elves) != self.num_elves:
                return None
            self.round_num += 1
        return self.get_result()

    def get_result(self):
        hps = [character.hp for character in self.characters()]
        return self.round_num * sum(hps)

    def make_move(self):
        for character in self.characters():
            if character in self.characters():
                to_attack = self.can_attack(character)
                if len(to_attack) == 0:
                    if not self.move(character):
                        return False
                    to_attack = self.can_attack(character)
                    if len(to_attack) > 0:
                        self.attack(character, to_attack)
                else:
                    self.attack(character, to_attack)
        return True

    def characters(self):
        characters = self.goblins + self.elves
        characters.sort()
        return characters

    def opponents(self, character):
        symbol = character.symbol
        if symbol == "G":
            return self.elves
        elif symbol == "E":
            return self.goblins
        else:
            raise Exception("Unknown symbol: {}".format(symbol))

    def can_attack(self, character):
        symbol = character.symbol
        adjacent = character.position.adjacent()

        to_attack = []
        for opponent in self.opponents(character):
            if opponent.position in adjacent:
                to_attack.append(opponent)
        to_attack.sort(key=attrgetter("hp", "position"))
        return to_attack

    def move(self, character):
        seen = [other.position for other in self.characters()]
        possibilities = self.get_possibilities(character, seen)
        if possibilities is None:
            return False

        if len(possibilities) > 0:
            closest = self.get_closest(character.position, possibilities, seen)
            if closest is not None:
                next_position = self.get_closest(
                    closest, self.adjacent(character.position, set(seen)), seen
                )
                character.position = next_position
        return True

    def get_possibilities(self, character, seen):
        opponents = self.opponents(character)
        if len(opponents) == 0:
            return None

        possibilities = []
        for opponent in opponents:
            possibilities.extend(self.adjacent(opponent.position, set(seen)))
        return possibilities

    def adjacent(self, position, seen=None):
        if seen is None:
            seen = set()

        result = []
        for adjacent in position.adjacent():
            if self.grid[adjacent] == "." and adjacent not in seen:
                result.append(adjacent)
        return result

    def get_closest(self, start, possibilities, seen):
        distances = []
        for possibility in possibilities:
            distance = self.distance(start, possibility, set(seen))
            if distance is not None:
                distances.append((possibility, distance))

        if len(distances) > 0:
            min_dist = min([distance[1] for distance in distances])
            minimums = [
                distance[0] for distance in distances if distance[1] == min_dist
            ]
            minimums.sort()
            return minimums[0]

    def distance(self, start, end, seen):
        queue = [(start, 0)]
        current = (None, None)

        while len(queue) > 0 and current[0] != end:
            current = queue.pop(0)
            for adjacent in self.adjacent(current[0], seen):
                queue.append((adjacent, current[1] + 1))
                seen.add(adjacent)

        return current[1] if current[0] == end else None

    def attack(self, character, to_attack):
        to_attack = to_attack[0]
        to_attack.attacked(character)
        if not to_attack.alive():
            self.remove(to_attack)

    def remove(self, character):
        symbol = character.symbol
        if symbol == "G":
            self.goblins.remove(character)
        elif symbol == "E":
            self.elves.remove(character)
        else:
            raise Exception("Unknown symbol: {}".format(symbol))

    def __getitem__(self, position):
        for character in self.characters():
            if character.position == position:
                return character
        return None

    def __contains__(self, position):
        return self[position] is not None

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = []
        for y, row in enumerate(str(self.grid).split("\n")):
            result_row = []
            for x, value in enumerate(row):
                position = Point(x, y)
                value = value if position not in self else self[position].symbol
                result_row.append(value)
            result.append("".join(result_row))
        return "\n".join(result)


def main():
    data = Parser().nested_lines()
    answer.part1(214731, play_game(data, False))
    answer.part2(53222, play_game(data, True))


def play_game(data, play_until_elf_win):
    if play_until_elf_win:
        attack, result = 10, None
        while result is None:
            attack += 1
            game = get_game(data, attack)
            result = game.play_until_elf_dies()
        return result
    else:
        game = get_game(data, 3)
        return game.play()


def get_game(data, attack):
    return Game(
        get_grid(data), get_characters(data, "G", 3), get_characters(data, "E", attack)
    )


def get_grid(data):
    grid = Grid()
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            point = Point(x, y)
            value = "#" if value == "#" else "."
            grid[point] = value
    return grid


def get_characters(data, symbol, attack):
    characters = []
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == symbol:
                point = Point(x, y)
                characters.append(Character(symbol, point, attack))
    return characters


if __name__ == "__main__":
    main()
