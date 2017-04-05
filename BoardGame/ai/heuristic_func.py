def simple(game, player):
    if game.winner is None:
        return 0
    elif game.winner == -1:
        return 0
    elif game.winner == player:
        return 1
    else:
        return -1
