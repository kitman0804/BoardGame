import numpy as np
from ..Player import Player
from ..GameTree import GameTree


class AlphaBeta(Player):
    is_ai = True
    def __init__(self, player=0, name='AB', n_depth=4, silent=True):
        super().__init__(player=player, name=name)
        self._n_depth = n_depth
        self._silent = silent
    
    def decide(self, game):
        tree = GameTree('current', game=game)
        tree.alpha_beta(depth=self._n_depth)
        if not self._silent:
            print(game.turn, 'root:', gt.root.game.turn_player)
            tree.show()
        moves_reward = [(child.name, child.reward) for child in tree.children]
        moves_reward.sort(key=lambda x: x[1])
        moves = [m for m, r in moves_reward if r == moves_reward[-1][1]]
        move = moves[np.random.choice(range(len(moves)))]
        return move
    
    def decide_ui(self, game_ui):
        move = self.decide(game=game_ui.game)
        game_ui.gameboard_buttons.get(move).click()
