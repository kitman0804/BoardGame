import sys
import functools
import numpy as np
from PyQt5.QtWidgets import (QApplication, qApp,
    QWidget, QDesktopWidget,
    QLabel, QComboBox, QPushButton,
    QGridLayout, QVBoxLayout,
    QSizePolicy)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QSize
from .TicTacToe import TicTacToe
from ..players import Human, Monkey, RobotTS
from ..ai import search
from ..ai.heuristic_func import HeuristicWDLN, HeuristicSimulate


REGISTERED_PLAYER_TYPES = (Human, Monkey, RobotTS)

PLAYERS = {
    'Human': Human(),
    'Monkey': Monkey(),
    'Robot-MM6': RobotTS(
        search_func=search.minimax,
        depth=6),
    'Robot-MM6-S': RobotTS(
        search_func=search.minimax,
        depth=6,
        use_symmetry=True),
    'Robot-AB6-S': RobotTS(
        search_func=search.alpha_beta,
        depth=6,
        use_symmetry=True),
    'Robot-MAB9-S': RobotTS(
        search_func=search.modified_alpha_beta,
        depth=6,
        use_symmetry=True),
}


class TicTacToeUIButton(QPushButton):
    def __init__(self, *args, style_sheet='', **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(100, 100)
        self.setIconSize(QSize(80, 80))
        size_policy = QSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Preferred
        )
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)
        self._style_sheet = style_sheet
        self.setStyleSheet(self._style_sheet)
    
    def heightForWidth(self, width):
        return width
    
    def add_border(self, style_sheet):
        self.setStyleSheet(self._style_sheet + style_sheet)
    
    def remove_border(self):
        self.setStyleSheet(self._style_sheet)
    
    def reset(self):
        self.setStyleSheet(self._style_sheet)
        self.setIcon(QIcon())


class TicTacToeUI(QWidget):
    m, n, k = 3, 3, 3
    icons = ['icons/x-mark.svg', 'icons/hollow-circle.svg']
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.init_ui()
        self._game = TicTacToe()
        self._started = False
    
    @property
    def game(self):
        return self._game
    
    @property
    def gameboard(self):
        return self._game.gameboard
    
    @property
    def gameboard_buttons(self):
        return self._gameboard_buttons
    
    @property
    def players(self):
        return self._game.players
    
    @property
    def turn_player(self):
        return self._game.turn_player
    
    def init_ui(self):
        self.center()
        self.setWindowTitle("TicTacToe")
        self.setStyleSheet('background-color: #D7CCC8;')
        # Players
        self._players_selector = QGridLayout()
        self._players = list()
        for p in range(2):
            label = QLabel('Player {:}'.format(p))
            l = list(PLAYERS.keys())
            l.sort()
            selectbox = QComboBox()
            selectbox.setFixedHeight(24)
            selectbox.addItems(l)
            self._players_selector.addWidget(label, 0, p)
            self._players_selector.addWidget(selectbox, 1, p)
            self._players.append(selectbox)
        self._grid = QGridLayout()
        self._gameboard_buttons = dict()
        for row in range(self.m):
            for col in range(self.n):
                btn = TicTacToeUIButton('', parent=self, style_sheet='background-color: #D7CCC8;')
                btn.clicked.connect(functools.partial(self.click_gameboard, row, col))
                self._grid.addWidget(btn, row, col)
                self._gameboard_buttons.update({(row, col): btn})
        self._message_box = QLabel('', parent=self)
        self._restart_button = QPushButton('Start', parent=self)
        self._restart_button.clicked.connect(self.restart)
        self._close_button = QPushButton('Close', parent=self)
        self._close_button.clicked.connect(self.close)
        # Layout
        self._layout = QVBoxLayout()
        self._layout.addLayout(self._players_selector)
        self._layout.addLayout(self._grid)
        self._layout.addWidget(self._message_box)
        self._layout.addWidget(self._restart_button)
        self._layout.addWidget(self._close_button)
        self.setLayout(self._layout)
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def click_gameboard(self, row, col):
        if not self._started or self._game.is_ended:
            pass
        else:
            btn = self._gameboard_buttons.get((row, col))
            if self.gameboard.array[row, col] != -1:
                msg = 'It is occupied. Please select another one.'
                self._message_box.setText(msg)
            else:
                for _, b in self._gameboard_buttons.items():
                    b.remove_border()
                btn.setIcon(QIcon(self.icons[self._game.turn_player]))
                btn.add_border('border: 1px solid #FF0000;')
                self._game.place_stone(row=row, col=col, player=self._game.turn_player)
                self._message_box.setText('')
            # Next turn
            self.next_turn()
    
    def next_turn(self):
        if self._game.is_ended:
            # Result
            if self._game.winner == -1:
                msg = 'Draw. What a game!'
            else:
                msg = 'Player {:} won. Congratulations!'
                msg = msg.format(self._game.winner)
            self._message_box.setText(msg)
        else:
            qApp.processEvents()
            self.players[self.turn_player].decide_ui(self)
    
    def reset(self):
        self._started = True
        self._game.reset()
        self._game.player0 = PLAYERS.get(self._players[0].currentText())
        self._game.player1 = PLAYERS.get(self._players[1].currentText())
        self._restart_button.setText('Restart')
        self._message_box.setText('')
        for _, btn in self._gameboard_buttons.items():
            btn.reset()
        # Start game
        qApp.processEvents()
        self.players[self.turn_player].decide_ui(self)
    
    def restart(self):
        self.reset()


def main():
    app = QApplication(sys.argv)
    widget = TicTacToeUI()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
