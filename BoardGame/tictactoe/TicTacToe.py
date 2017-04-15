from ..prototype.mnkgame.Game import Game


class TicTacToe(Game):
    def __init__(self):
        super().__init__(m=3, n=3, k=3)
