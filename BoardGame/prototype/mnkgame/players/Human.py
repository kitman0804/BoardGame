import numpy as np
from .Player import Player
from ..ai import GameTree, search, heuristic


class Human(Player):
    is_ai = False
    def __init__(self, name='Human', stone=0, hint=False):
        super().__init__(name=name, stone=stone)
        self._hint = hint
    
    @staticmethod
    def get_hint(game):
        tree = GameTree('current', game=game)
        search.minmax(
            node=tree,
            depth=2,
            hfunc=heuristic.Simple,
            use_symmetry=False
        )
        coords_reward = [(child.name, child.reward) for child in tree.children]
        best_reward = max(r for _, r in coords_reward)
        coord_choices = [m for m, r in coords_reward if r == best_reward]
        return tree, coord_choices
    
    def decide(self, game):
        print(game.gameboard.array)
        if self._hint:
            tree, coord_choices = self.get_hint(game)
            print('You are player {:}.'.format(game.turn_player))
            tree.show(1)
            print('Suggestions:')
            print(coord_choices)
        coord = input('{:}, what\'s your decision? '.format(self.name))
        if coord.lower() == 'p':
            return 'pause'
        else:
            try:
                coord = eval(coord)
            except NameError:
                coord = None
        return coord
    
    def decide_ui(self, game_ui):
        pass
