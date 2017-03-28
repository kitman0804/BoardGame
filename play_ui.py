import sys
from PyQt5 import QtWidgets
from BoardGame.tictactoe import TicTacToeUI


def main():
    if 'tictactoe' in sys.argv:
        app = QtWidgets.QApplication(sys.argv)
        widget = TicTacToeUI()
        widget.show()
        sys.exit(app.exec_())
    else:
        print('What game do you want to play?')


if __name__ == '__main__':
    main()
