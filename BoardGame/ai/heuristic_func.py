import numpy as np

def simple(game, player, reward_param=(1, 0, -1, 0)):
    if game.winner is None:
        return reward_param[-1]
    elif game.winner == -1:
        return reward_param[1]
    elif game.winner == player:
        return reward_param[0]
    else:
        return reward_param[2]


def simulation(game, player, n_sim=10, reward_param=(1, 0, -1)):
    if game.winner is None:
        simulated_games = []
        reward = 0
        for _ in range(n_sim):
            game_s = game.copy()
            while not game_s.is_ended:
                coords = game_s.gameboard.all_available_coords
                coord = coords[np.random.choice(len(coords))]
                game_s.place_stone(*coord, game_s.turn_player)
            if game_s.winner == -1:
                reward += reward_param[-1]
            elif game_s.winner == player:
                reward += reward_param[0]
            else:
                reward += reward_param[2]
        return reward / n_sim
    elif game.winner == -1:
        return reward_param[-1]
    elif game.winner == player:
        return reward_param[0]
    else:
        return reward_param[2]
