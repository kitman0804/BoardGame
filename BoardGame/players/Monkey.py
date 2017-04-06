import numpy as np
from ..Player import Player


class Monkey(Player):
    is_ai = True
    def __init__(self, name='Money', player=0, silent=True):
        super().__init__(player=player, name=name)
        self._silent = silent
    
    def decide(self, game):
        coord_choices = game.gameboard.all_coord_choices
        coord = coord_choices[np.random.choice(len(coord_choices))]
        return coord
    
    def decide_ui(self, game_ui):
        coord = self.decide(game=game_ui.game)
        game_ui.gameboard_buttons.get(coord).click()
