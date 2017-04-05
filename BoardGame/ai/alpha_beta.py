import numpy as np


def alpha_beta(tree, hfunc, alpha=-np.inf, beta=np.inf):
    if tree.is_leaf:
        root_player = tree.root.game.turn_player
        tree.reward = hfunc(game=tree.game, player=root_player)
    elif tree.depth % 2 == 0:
        best_value = -np.inf
        for child in tree.children:
            alpha_beta(tree=child, hfunc=hfunc, alpha=alpha, beta=beta)
            best_value = max(best_value, child.reward)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        tree.reward = best_value
    else:
        best_value = np.inf
        for child in tree.children:
            alpha_beta(tree=child, hfunc=hfunc, alpha=alpha, beta=beta)
            best_value = min(best_value, child.reward)
            beta = max(beta, best_value)
            if beta <= alpha:
                break
        tree.reward = best_value
