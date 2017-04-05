import numpy as np
from ..Player import Player
from ..ai import GameTree
from PyQt5.QtWidgets import qApp


class Human(Player):
    is_ai = False
    def __init__(self, name='Human', player=0, hint=False):
        super().__init__(player=player, name=name)
        self._hint = hint
    
    def decide(self, game):
        print(game.gameboard.gameboard)
        move = input('{:}, what is your move? '.format(self.name))
        if move.lower() == 'p':
            return 'pause'
        else:
            try:
                move = eval(move)
            except NameError:
                move = None
        return move
    
    def decide_ui(self, game_ui):
        pass
