import numpy as np
from ..Player import Player
from ..ai import GameTree, search, heuristic_func


class AlphaBeta(Player):
    is_ai = True
    def __init__(self, player=0, name='AB',
                 depth=4, hfunc=heuristic_func.simple, use_symmetry=False,
                 silent=True):
        super().__init__(player=player, name=name)
        self._depth = depth
        self._hfunc = hfunc
        self._use_symmetry = use_symmetry
        self._silent = silent
    
    def decide(self, game):
        tree = GameTree('current', game=game)
        search.alpha_beta(
            node=tree,
            depth=self._depth,
            hfunc=self._hfunc,
            use_symmetry=self._use_symmetry
        )
        coords_reward = [(child.name, child.reward) for child in tree.children]
        best_reward = max(r for _, r in coords_reward)
        coord_choices = [m for m, r in coords_reward if r == best_reward]
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
