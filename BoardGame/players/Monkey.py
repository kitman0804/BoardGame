import numpy as np
from ..Player import Player


class Monkey(Player):
    is_ai = True
    def __init__(self, name='Money', player=0, silent=True):
        super().__init__(player=player, name=name)
        self._silent = silent
    
    def decide(self, game):
        available_coords = game.gameboard.available_coords
        move = available_coords[np.random.choice(len(available_coords))]
        return move
    
    def decide_ui(self, game_ui):
        move = self.decide(game=game_ui.game)
        game_ui.gameboard_buttons.get(move).click()
