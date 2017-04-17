import numpy as np
from .Player import Player
from ..ai import GameTree, heuristic
from ..ai.search import *


class RobotTS(Player):
    is_ai = True
    def __init__(self, name='R0bot', stone=0,
                 search_method=Minimax(
                    hfunc=heuristic.Simple().evaluate,
                    use_symmetry=True),
                 depth=4,
                 silent=True):
        super().__init__(name=name, stone=stone)
        self._search_method = search_method
        self._depth = depth
        self._silent = silent
    
    def decide(self, game):
        tree = GameTree('current', game_core=game.core)
        self._search_method.search(node=tree, depth=self._depth)
        coords_reward = [(child.name, child.reward) for child in tree.children]
        best_reward = max(r for _, r in coords_reward)
        best_coords = [m for m, r in coords_reward if r == best_reward]
        if self._search_method.use_symmetry:
            coord_choices = list()
            for x in best_coords:
                coord_choices.extend(game.gameboard.equivalent_coords_dict.get(x, [x]))
            coord_choices = list(set(coord_choices))
        else:
            coord_choices = best_coords
        coord = coord_choices[np.random.choice(range(len(coord_choices)))]
        if not self._silent:
            print(game.turn)
            print('root:', tree.root_player)
            print(game.gameboard.array)
            tree.show(1)
            print(coord_choices)
        return coord
    
    def decide_ui(self, game_ui):
        coord = self.decide(game=game_ui.game)
        game_ui.gameboard_buttons.get(coord).click()
