class Game:

    def __init__(self, deck1, deck2, recursive=False):
        self.deck1 = deck1
        self.deck2 = deck2
        self.recursive = recursive
        self.states = set()

    def play(self):
        winner = self.get_winner()
        return self.deck1 if winner == 1 else self.deck2

    def get_winner(self):
        while not self.deck1.empty() and not self.deck2.empty():
            # Prevents infnity
            if not self.update_state():                
                return self.deck1.identifier

            card1 = self.deck1.next()
            card2 = self.deck2.next()

            if self.recursive and card1 <= len(self.deck1) and card2 <= len(self.deck2):
                winner = Game(self.deck1.copy(card1), self.deck2.copy(card2), self.recursive).get_winner()
            else:
                winner = self.deck1.identifier if card1 > card2 else self.deck2.identifier

            self.deck1.add([card1, card2]) if winner == 1 else self.deck2.add([card2, card1])

        return self.deck2.identifier if self.deck1.empty() else self.deck1.identifier

    def update_state(self):
        state = str(self.deck1) + str(self.deck2)
        if state in self.states:
            return False
        else:
            self.states.add(state)
            return True


class Deck:

    def __init__(self, cards, identifier):
        self.cards = [int(card) for card in cards]
        self.identifier = identifier

    def empty(self):
        return len(self.cards) == 0

    def next(self):
        card = self.cards[0]
        self.cards = self.cards[1:]
        return card

    def add(self, cards):
        self.cards += cards

    def score(self):
        score = 0
        for i, card in enumerate(self.cards):
            multiplier = len(self.cards) - i
            score += (multiplier * card)
        return score

    def copy(self, n):
        cards = [card for card in self.cards]
        return Deck(cards[:n], self.identifier)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.cards)


def main():
    # Part 1: 32102
    print('Part 1: {}'.format(run_game(False)))
    # Part 2: 34173
    print('Part 2: {}'.format(run_game(True)))


def run_game(recursive):
    game = Game(*get_decks(), recursive)
    winner = game.play()
    return winner.score()


def get_decks():
    file_name = 'data'
    with open('{}.txt'.format(file_name), 'r') as f:
        data = f.read().splitlines()
    split = data.index('')
    return Deck(data[1:split], 1), Deck(data[split+2:], 2)


if __name__ == '__main__':
    main()
