import sys
from PyQt5.QtWidgets import QApplication, qApp
from BoardGame.tictactoe import TicTacToeUI
from BoardGame.connectfour import ConnectFourUI


def main():
    game_type = ('tictactoe', 'connectfour')
    try:
        game = sys.argv[1]
    except IndexError:
        game = None
    while game not in game_type:
        query = (
            'What game do you want to play? \n'
            '(tictactoe, connectfour) '
        )
        game = input(query).lower()
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
        pass


if __name__ == '__main__':
    main()
