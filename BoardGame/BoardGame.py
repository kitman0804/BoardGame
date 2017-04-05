from copy import deepcopy
from .GameRecorder import GameRecorder


class BoardGame(object):
    category = ''
    n_players = None
    
    def __init__(self):
        self._players = []
        self._gameboard = None
        self.available_coords = ()
        self._turn = None
        self._winner = None
        self._recorder = GameRecorder()
    
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
    
    def record(coord, player):
        self._recorder.record(coord=coord, player=player)
    
    def save_record(self, directory, game_id):
        path = directory + '/' + game_id + '.json'
        msg = 'The record is saved in {:}'.format(path)
        print(msg)
        self._recorder.save_json(path)
