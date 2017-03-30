from copy import deepcopy


class BoardGame(object):
    category = ''
    n_players = None
    
    def __init__(self):
        self._players = []
        self._gameboard = None
        self.available_moves = ()
        self._turn = None
        self._winner = None
    
    @property
    def gameboard(self):
        return self._gameboard
    
    @property
    def turn(self):
        return self._turn
    
    @property
    def winner(self):
        return self._winner
    
    @property
    def is_ended(self):
        return self._winner is not None or self._turn is None
    
    def copy(self):
        return deepcopy(self)
