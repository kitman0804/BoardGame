import numpy as np


class Simple(object):
    def __init__(self, w=1, d=0, l=-1, not_ended=0):
        # Reward parameters
        self.w = w
        self.d = d
        self.l = l
        self.not_ended = not_ended
    
    def evaluate(self, game, player):
        if game.winner is None:
            return self.not_ended
        elif game.winner == -1:
            return self.d
        elif game.winner == player:
            return self.w
        else:
            return self.l


class Simulate(object):
    def __init__(self, w=1, d=0, l=-1, n_sim=10):
        # Reward parameters
        self.w = w
        self.d = d
        self.l = l
        # Number of simulation
        self.n_sim = n_sim
    
    def evaluate(self, game, player):
        if game.winner is None:
            simulated_games = []
            reward = 0
            for _ in range(self.n_sim):
                game_s = game.copy()
                while not game_s.is_ended:
                    coords = game_s.gameboard.available_coords
                    coord = coords[np.random.choice(len(coords))]
                    game_s.place_stone(*coord, game_s.current_player)
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
