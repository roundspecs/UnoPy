from random import randint
from uno_func import input_cls
from os import system


class UnoError(Exception):
    pass


class Card():
    def __init__(self, color, num=''):
        self.color = color
        self.num = num

    def show(self, sep='\t'):
        print(f'{self.color}{sep}{self.num}')


class Deck():
    cards = [
        Card(color, num)
        for color in ['RED', 'GREEN', 'BLUE', 'YELLOW']
        for num in ['0'] +
                   ['+2', 'skip', 'reverse']*2 +
        list(range(1, 10))*2
    ] + [Card('WILD')]*4 + [Card('WILD', '+4')]*4

    def __init__(self):
        self.shuffle()

    def shuffle(self):
        len_cards = len(self.cards)
        for card_index in range(len_cards):
            rand_index = randint(0, len_cards-1)
            self.cards[card_index], self.cards[rand_index] = self.cards[rand_index], self.cards[card_index]

    def show(self):
        for card in self.cards:
            card.show()

    def add(self, card):
        self.cards.append(card)
        self.shuffle()


class Board():
    card = None

    def __init__(self, deck):
        self.deck = deck

        # first board card should not be +4, WILD, +2, skip or reverse
        for card_index in range(len(self.deck.cards)):
            if (self.deck.cards[card_index].num not in ['', '+4', '+2', 'skip', 'reverse']):
                self.card = deck.cards.pop(card_index)
                break
            else:
                raise UnoError('No suitable board card found')

    def show(self):
        print('Board card: ', end='')
        self.card.show(sep=' ')


class Player():

    players = []
    deck = None
    board = None

    def __init__(self, name, deck, board):
        self.name = name.title()
        self.players.append(self)
        self.hand = []
        self.deck = deck
        self.board = board
        self.draw(7)

    def show_hand(self):
        self.board.show()
        print(f"{self.name}'s turn")
        for card_index, card in enumerate(self.hand, 1):
            print(f'({card_index}) -> ', end='')
            card.show()

    def draw(self, num):
        for _ in range(num):
            self.hand.append(self.deck.cards.pop())

    def pick_a_card(self):
        color = self.board.card.color
        num = self.board.card.num
        if not (
            'WILD' in [card.color for card in self.hand] or
            color in [card.color for card in self.hand] or
            num in [card.num for card in self.hand]
        ):
            self.draw(1)
            raise UnoError("You picked a card")
        raise UnoError("Unable to draw card")

    def play_card(self):
        self.show_hand()
        input_str = input()

        if input_str == 'draw':
            self.pick_a_card()

        card_index = int(input_str) - 1
        if card_index < 0:
            raise UnoError('Invalid number')
        played_card = self.hand[card_index]

        if not (
            played_card.color == "WILD" or
            played_card.color == self.board.card.color or
            played_card.num == self.board.card.num
        ):
            raise UnoError('Invalid card')

        if played_card.color == 'WILD':
            color_index = -1
            while not (-1 < color_index < 4):
                color_index = int(
                    input_cls('Enter a color:\n1. RED\n2. GREEN\n3. BLUE\n4. YELLOW\n')) - 1
            played_card.color = ['RED', 'GREEN', 'BLUE', 'YELLOW'][color_index]
        else:
            system('cls')
        self.deck.add(self.board.card)
        self.board.card = self.hand.pop(card_index)

    def turn_welcome(self):
        self.board.show()
        print(f"{self.name}'s turn")
        input_cls()

