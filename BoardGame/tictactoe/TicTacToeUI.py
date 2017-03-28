import sys
import functools
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from .TicTacToe import TicTacToe
from .players import Human, Monkey, MinMax, MinMaxSim


REGISTER_PLAYER_TYPES = (Human, Monkey, MinMax, MinMaxSim)

PLAYERS = {
    'Human': Human(),
    'Monkey': Monkey(),
    'MM2': MinMax(n_depth=2),
    'MM4': MinMax(n_depth=4),
    'MMS2.20': MinMaxSim(n_depth=2, n_sim=20),
    'MMS2.50': MinMaxSim(n_depth=2, n_sim=50),
    'MMS4.01': MinMaxSim(n_depth=4, n_sim=1),
}


class TicTacToeUIButton(QtWidgets.QPushButton):
    def __init__(self, *args, style_sheet='', **kwargs):
        super().__init__(*args, **kwargs)
        self._occupied_player = -1
        self._style_sheet = style_sheet
        self.setStyleSheet(self._style_sheet)
    
    @property
    def occupied_player(self):
        return self._occupied_player
    
    @occupied_player.setter
    def occupied_player(self, x):
        if x in (-1, 0, 1):
            self._occupied_player = x
        else:
            raise ValueError('occupied player can only be -1 or 0 or 1.')
    
    @property
    def is_occupied(self):
        return self._occupied_player != -1
    
    def add_border(self, style_sheet):
        self.setStyleSheet(self._style_sheet + style_sheet)
    
    def remove_border(self):
        self.setStyleSheet(self._style_sheet)
    
    def reset(self):
        self._occupied_player = -1
        self.setStyleSheet(self._style_sheet)
        self.setIcon(QtGui.QIcon())


class TicTacToeUI(QtWidgets.QWidget):
    m, n, k = 3, 3, 3
    icons = ['icons/x-mark.png', 'icons/hollow-circle.png']
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TicTacToe")
        self.setStyleSheet('background-color: #D7CCC8;')
        # Players
        self._players_selector = QtWidgets.QGridLayout()
        self._players = list()
        for p in range(2):
            label = QtWidgets.QLabel('Player {:}'.format(p))
            l = list(PLAYERS.keys())
            l.sort()
            selectbox = QtWidgets.QComboBox()
            selectbox.setFixedHeight(24)
            selectbox.addItems(l)
            self._players_selector.addWidget(label, 0, p)
            self._players_selector.addWidget(selectbox, 1, p)
            self._players.append(selectbox)
        self._grid = QtWidgets.QGridLayout()
        self._gameboard_buttons = dict()
        for i in range(self.m):
            for j in range(self.n):
                btn = self.create_gameboard_button(row=i, col=j)
                self._grid.addWidget(btn, i, j)
                self._gameboard_buttons.update({(i, j): btn})
        self._message_box = QtWidgets.QLabel('', parent=self)
        self._restart_button = QtWidgets.QPushButton('Start', parent=self)
        self._restart_button.setFixedHeight(32)
        self._restart_button.clicked.connect(self.restart)
        # Layout
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addLayout(self._players_selector)
        self._layout.addLayout(self._grid)
        self._layout.addWidget(self._message_box)
        self._layout.addWidget(self._restart_button)
        self.setLayout(self._layout)
        # The game
        self._game = TicTacToe()
        self._started = False
    
    @property
    def game(self):
        return self._game
    
    @property
    def gameboard_buttons(self):
        return self._gameboard_buttons
    
    def create_gameboard_button(self, row, col):
        btn = TicTacToeUIButton('', parent=self, style_sheet='background-color: #D7CCC8;')
        btn.setFixedSize(64, 64)
        btn.clicked.connect(functools.partial(self.click, row, col))
        return btn
    
    def click(self, row, col):
        if not self._started:
            pass
        elif self._game.is_ended:
            pass
        else:
            btn = self._gameboard_buttons.get((row, col))
            if btn is not None:
                if btn.is_occupied:
                    msg = 'It is occupied. Please select another one.'
                    self._message_box.setText(msg)
                else:
                    player = self._game.turn_player
                    # Icon appearance
                    for _, b in self._gameboard_buttons.items():
                        b.remove_border()
                    btn.setIcon(QtGui.QIcon(self.icons[player]))
                    btn.setIconSize(QtCore.QSize(48, 48))
                    btn.add_border('border: 1px solid #FF0000;')
                    btn.occupied_player = player
                    # Check result
                    self._game.move(row=row, col=col, player=player)
                    if self._game.winner is not None:
                        if self._game.winner == -1:
                            msg = 'Draw. What a game!'
                        else:
                            msg = 'Player {:} won. Congratulations!'
                            msg = msg.format(self._game.winner)
                    else:
                        msg = ''
                    self._message_box.setText(msg)
            # Next turn
            if self._game.is_ended:
                pass
            else:
                self._game.players[self._game.turn_player].decide_ui(self)
    
    def reset(self):
        self._started = True
        self._game.reset()
        self._game.player0 = PLAYERS.get(self._players[0].currentText())
        self._game.player1 = PLAYERS.get(self._players[1].currentText())
        self._restart_button.setText('Restart')
        self._message_box.setText('')
        for _, btn in self._gameboard_buttons.items():
            btn.reset()
        if self._game.player0.is_ai:
            self._game._player0.decide_ui(self)
    
    def restart(self):
        self.reset()


def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = TicTacToeUI()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
