import sys
from PyQt5.QtWidgets import QApplication, qApp
from BoardGame.tictactoe import TicTacToeUI
from BoardGame.connectfour import ConnectFourUI


AVAILABLE_GAMES = ('tictactoe', 'connectfour')

GAME_DICT = (
    '--------------------------------\n'
    'Game            Code\n'
    '--------------------------------\n'
    'Tic-Tac-Toe     tictactoe\n'
    'Connect Four    connectfour\n'
    '--------------------------------\n'
)

HELP_DOC = (
    '----------------------------------------------------------------\n'
    'If you want to play a game, you just simply need to type the\n'
    'game code.\n'
    'E.g. tictactoe for Tic-Tac-Toe\n'
    '----------------------------------------------------------------\n'
    'Other Commands:\n'
    'Help:            h\n'
    'Game Dictionary: d\n'
    'Quit:            q\n'
    '----------------------------------------------------------------\n'
)


def main():
    try:
        game = sys.argv[1]
    except IndexError:
        game = None
    # Query
    if game is None:
        print(GAME_DICT)
        while game is None:
            query = (
                'Which game do you want to play? \n'
                'Please type the code (Help: h)> '
            )
            game = input(query).lower()
            # Proceed
            if game == 'h':
                print(HELP_DOC)
                game = None
            elif game == 'd':
                print(GAME_DICT)
                game = None
            elif game == 'q':
                print('Byebye.')
                break
            elif game in AVAILABLE_GAMES:
                break
            else:
                print('Invalid input \'{:}\'.'.format(game))
                game = None
    # Start game
    if game == 'tictactoe':
        app = QApplication(sys.argv)
        widget = TicTacToeUI()
        widget.show()
        sys.exit(app.exec_())
    elif game == 'connectfour':
        app = QApplication(sys.argv)
        widget = ConnectFourUI()
        widget.show()
        sys.exit(app.exec_())
    else:
        print('No such game - {:}.'.format(game))
    

if __name__ == '__main__':
    main()
