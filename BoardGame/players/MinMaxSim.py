import numpy as np
from ..Player import Player
from ..GameTree import GameTree


class MinMaxSim(Player):
    is_ai = True
    def __init__(self, player=0, name='MMS', n_depth=4, n_sim=10, silent=True):
        super().__init__(player=player, name=name)
        self._n_depth = n_depth
        self._n_sim = n_sim
        self._silent = silent
    
    def decide(self, game):
        tree = GameTree('current', game=game)
        tree.minmax(depth=self._n_depth)
        tree.monte_carlo(r=self._n_sim)
        if not self._silent:
            print(game.turn, 'root:', tree.root.game.turn_player)
            tree.show(1)
        moves_reward = [(child.name, child.reward) for child in tree.children]
        moves_reward.sort(key=lambda x: x[1])
        moves = [m for m, r in moves_reward if r == moves_reward[-1][1]]
        move = moves[np.random.choice(range(len(moves)))]
        return move
        
    def decide_ui(self, game_ui):
        move = self.decide(game=game_ui.game)
        game_ui.gameboard_buttons.get(move).click()
