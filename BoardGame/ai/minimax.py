import numpy as np


def minimax(tree, hfunc):
    if tree.is_leaf:
        root_player = tree.root.game.turn_player
        tree.reward = hfunc(game=tree.game, player=root_player)
    elif tree.depth % 2 == 0:
        best_value = -np.inf
        for child in tree.children:
            minimax(tree=child, hfunc=hfunc)
            best_value = max(best_value, child.reward)
        tree.reward = best_value
    else:
        best_value = np.inf
        for child in tree.children:
            minimax(tree=child, hfunc=hfunc)
            best_value = min(best_value, child.reward)
        tree.reward = best_value
