import sys
from PyQt5.QtWidgets import QApplication, qApp
from BoardGame.tictactoe import TicTacToeUI
from BoardGame.connectfour import ConnectFourUI


def main():
    if 'tictactoe' in sys.argv:
        app = QApplication(sys.argv)
        widget = TicTacToeUI()
        widget.show()
        sys.exit(app.exec_())
    elif 'connectfour' in sys.argv:
        app = QApplication(sys.argv)
        widget = ConnectFourUI()
        widget.show()
        sys.exit(app.exec_())
    else:
        print('What game do you want to play?')


if __name__ == '__main__':
    main()
