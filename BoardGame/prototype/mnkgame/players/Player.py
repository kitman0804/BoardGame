class Player(object):
    def __init__(self, name='Player', stone=0):
        self.name = name
        self._stone = stone
    
    @property
    def stone(self):
        return self._stone
    
    @stone.setter
    def stone(self, x):
        if not isinstance(x, int):
            raise ValueError('stone must be an non-negative integer.')
        elif x < 0:
            raise ValueError('stone must be an non-negative integer.')
        else:
            self._stone = x
