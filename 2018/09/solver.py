from collections import deque

import commons.answer as answer


class Player:

    def __init__(self, id):
        self.id = id
        self.score = 0

    def add_score(self, value):
        self.score += value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{}: {}'.format(self.id, self.score)


class Game:

    def __init__(self, num_players):
        self.players = [Player(i + 1) for i in range(num_players)]
        self.board = deque([0])

    def play(self, moves):
        for i in range(moves):
            value = i + 1
            if value % 23 == 0:
                self.board.rotate(-6)
                player = self.players[i % len(self.players)]
                player.add_score(value)
                value = self.board.popleft()
                player.add_score(self.board.popleft())
            else:
                self.board.rotate(1)
            self.board.appendleft(value)
        
    def get_high_score(self):
        scores = [player.score for player in self.players]
        return max(scores)
                
    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.board)


def main():
    num_players = 411
    highest_value = 72_059
    answer.part1(429943, solve(num_players, highest_value))
    answer.part2(3615691746, solve(num_players, highest_value * 100))


def solve(num_players, num_moves):
    game = Game(num_players)
    game.play(num_moves)
    return game.get_high_score()


if __name__ == '__main__':
    main()
