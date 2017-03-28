class Player(object):
    def __init__(self, name='Player', player=0):
        self._player = player
        self.name = name
    
    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, x):
        if x not in [0, 1]:
            raise ValueError('player must be 0 (1st player) or 1 (2nd player).')
        else:
            self._player = x
