from uno_classes import Deck, Player, Board
from os import system
from uno_func import clear_screen, input_cls

system('cls')

# create deck
deck = Deck()
# create board
board = Board(deck)


# promt players
@clear_screen
def input_players():
    player_num = int(input('Number of players: '))
    for player_index in range(player_num):
        Player(
            input(f'Name of player-{player_index+1}: '),
            deck, board
        )


# create players
input_players()

game_over = False

direction = 1  # default -> 1, reverse -> -1

while not game_over:
    show_turn_msg = True
    player_index = 0
    while abs(player_index) < len(Player.players):
        player = Player.players[player_index]
        if show_turn_msg:
            player.turn_welcome()
        else:
            show_turn_msg = True
        board_card_num = player.board.card.num
        try:
            if board_card_num == 'skip':
                player.board.card.num += ' '
            elif board_card_num == 'reverse':
                direction = -1 if direction == 1 else 1
                player_index += direction
                player.board.card.num += ' '
            elif board_card_num == '+2':
                player.board.card.num += ' '
                player.draw(2)
            elif board_card_num == '+4':
                player.board.card.num += ' '
                player.draw(4)
            else:
                player.play_card()
            player_index += direction
        except KeyboardInterrupt:
            if input('Exit?(y/n) ').upper() == 'Y':
                exit(f'Terminated by {player.name}')
        except Exception as e:
            system('cls')
            print(f'{e}. Try again.')
            show_turn_msg = False
