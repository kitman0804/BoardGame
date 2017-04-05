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
from .ConnectFour import ConnectFour
from ..players import Human, Monkey, MinMax, AlphaBeta


REGISTER_PLAYER_TYPES = (
    Human, Monkey, MinMax, AlphaBeta
)

PLAYERS = {
    'Human': Human(),
    'Monkey': Monkey(),
    'Robot-MM4': MinMax(n_depth=4),
    'Robot-MM6': MinMax(n_depth=6),
    'Robot-AB6': AlphaBeta(n_depth=6),
}


class ColumnButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(50, 50)
        self.setIconSize(QSize(32, 32))
        self.setIcon(QIcon('icons/down-arrow.svg'))
        self.click_count = 0
        self.clicked.connect(self.count)
    
    def count(self):
        self.click_count += 1
        if self.click_count > 6:
            self.setIcon(QIcon(''))
    
    def reset(self):
        self.setIcon(QIcon('icons/down-arrow.svg'))
        self.click_count = 0


class GameBoardButton(QPushButton):
    def __init__(self, *args, style_sheet='', **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(50, 50)
        self.setIconSize(QSize(32, 32))
        self.setIcon(QIcon(''))
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
        self.setIcon(QIcon(''))


class ConnectFourUI(QWidget):
    m, n, k = 6, 7, 4
    icons = [
        'icons/filled-circle-yellow.svg',
        'icons/filled-circle-red.svg'
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.init_ui()
        self._game = ConnectFour()
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
    
    @property
    def column_buttons(self):
        return self._column_buttons
    
    def init_ui(self):
        self.center()
        self.setWindowTitle("Connect Four")
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
        self._columns = QGridLayout()
        self._column_buttons = dict()
        self._grid = QGridLayout()
        self._gameboard_buttons = dict()
        for col in range(self.n):
            col_btn = ColumnButton('', parent=self)
            col_btn.clicked.connect(functools.partial(self.click_column, col))
            self._columns.addWidget(col_btn, 0, col)
            self._column_buttons.update({col: col_btn})
            for row in range(self.m):
                btn = GameBoardButton('', parent=self)
                btn.clicked.connect(col_btn.click)
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
        self._layout.addLayout(self._columns)
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
    
    def click_column(self, col):
        if not self._started or self._game.is_ended:
            pass
        else:
            row = self._column_buttons.get(col).click_count - 1
            btn = self._gameboard_buttons.get((self.m - 1 - row, col))
            if self.gameboard.array[row, col] != -1:
                msg = 'The column is fulled. Please select another one.'
                self._message_box.setText(msg)
            else:
                for _, b in self._gameboard_buttons.items():
                    b.remove_border()
                btn.setIcon(QIcon(self.icons[self.turn_player]))
                btn.add_border('border: 1px solid #FF0000;')
                self._game.place_stone(row=row, col=col, player=self.turn_player)
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
        for _, btn in self._column_buttons.items():
            btn.reset()
        for _, btn in self._gameboard_buttons.items():
            btn.reset()
        # Start game
        qApp.processEvents()
        self.players[self.turn_player].decide_ui(self)
    
    def restart(self):
        self.reset()
