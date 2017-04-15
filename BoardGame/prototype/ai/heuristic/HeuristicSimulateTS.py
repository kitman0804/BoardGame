import numpy as np
from .. import GameTree, search
from .HeuristicWDLN import HeuristicWDLN


class HeuristicSimulateTS(object):
    def __init__(self, w=1, d=0, l=-1, n_sim=10, depth=2):
        # Reward parameters
        self.w = w
        self.d = d
        self.l = l
        # Number of simulation
        self.n_sim = n_sim
        self.depth = depth
    
    def evaluate(self, game, player):
        if game.winner is None:
            simulated_games = []
            reward = 0
            for _ in range(self.n_sim):
                game_s = game.copy()
                while not game_s.is_ended:
                    tree = GameTree('root', game=game_s)
                    search.modified_alpha_beta(
                        tree,
                        depth=self.depth,
                        hfunc=HeuristicWDLN().evaluate,
                        use_symmetry=True
                    )
                    coords_reward = [(child.name, child.reward) for child in tree.children]
                    best_reward = max(r for _, r in coords_reward)
                    best_coords = [m for m, r in coords_reward if r == best_reward]
                    coord_choices = list()
                    for x in best_coords:
                        coord_choices.extend(game_s.gameboard.equivalent_coords.get(x, [x]))
                    coord_choices = list(set(coord_choices))
                    coord = coord_choices[np.random.choice(range(len(coord_choices)))]
                    game_s.place_stone(*coord, game_s.turn_player)
                if game_s.winner == -1:
                    reward += self.d
                elif game_s.winner == player:
                    reward += self.w
                else:
                    reward += self.l
            return reward / self.n_sim
        elif game.winner == -1:
            return self.d
        elif game.winner == player:
            return self.w
        else:
            return self.l
