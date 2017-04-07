import numpy as np
from ..Player import Player
from ..ai import GameTree, search
from BoardGame.ai.heuristic_func import HeuristicWDLN


class RobotTS(Player):
    is_ai = True
    def __init__(self, player=0, name='R0bot',
                 search_func=search.modified_alpha_beta,
                 depth=4, hfunc=HeuristicWDLN().evaluate, use_symmetry=False,
                 silent=True):
        super().__init__(player=player, name=name)
        self._search_func = search_func
        self._depth = depth
        self._hfunc = hfunc
        self._use_symmetry = use_symmetry
        self._silent = silent
    
    def decide(self, game):
        tree = GameTree('current', game=game)
        self._search_func(
            node=tree,
            depth=self._depth,
            hfunc=self._hfunc,
            use_symmetry=self._use_symmetry
        )
        coords_reward = [(child.name, child.reward) for child in tree.children]
        best_reward = max(r for _, r in coords_reward)
        best_coords = [m for m, r in coords_reward if r == best_reward]
        if self._use_symmetry:
            coord_choices = list()
            for x in best_coords:
                coord_choices.extend(game.gameboard.equivalent_coords.get(x, [x]))
            coord_choices = list(set(coord_choices))
        else:
            coord_choices = best_coords
        coord = coord_choices[np.random.choice(range(len(coord_choices)))]
        if not self._silent:
            print(game.turn)
            print('root:', tree.root.game.turn_player)
            print(game.gameboard.array)
            tree.show(1)
            print(coord_choices)
        return coord
    
    def decide_ui(self, game_ui):
        coord = self.decide(game=game_ui.game)
        game_ui.gameboard_buttons.get(coord).click()
