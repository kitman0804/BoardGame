class HeuristicWDLN(object):
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
