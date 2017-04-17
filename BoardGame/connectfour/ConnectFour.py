from ..prototype.mnkgame.Game import Game
from .GameBoard import GameBoard


class ConnectFour(Game):
    def __init__(self):
        super().__init__(m=6, n=7, k=4)
        self._core.gameboard = GameBoard()
