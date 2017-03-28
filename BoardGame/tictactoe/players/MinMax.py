import numpy as np
from ...Player import Player
from ..GameTree import GameTree


class MinMax(Player):
    is_ai = True
    def __init__(self, player=0, name='MM', n_depth=4, silent=True):
        super().__init__(player=player, name=name)
        self._n_depth = n_depth
        self._silent = silent
    
    def decide(self, game):
        gt = GameTree(game=game)
        gt.expand(depth=self._n_depth)
        if not self._silent:
            print(game.turn, 'root:', gt.root.game.turn_player)
            gt.show()
        move_reward = [(child.name, child.reward) for child in gt.root.children]
        move_reward.sort(key=lambda x: x[1])
        moves = [m for m, r in move_reward if r == move_reward[-1][1]]
        move = moves[np.random.choice(range(len(moves)))]
        return move
    
    def decide_ui(self, game_ui):
        move = self.decide(game=game_ui.game)
        game_ui.gameboard_buttons.get(move).click()
