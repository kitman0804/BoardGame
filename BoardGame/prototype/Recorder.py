import json


class Recorder(object):
    def __init__(self):
        self._turns = []
        self._winner = None
    
    @property
    def turns(self):
        return self._turns
    
    @property
    def winner(self):
        return self._winner
    
    @winner.setter
    def winner(self, x):
        self._winner = x
    
    def record(self, coord, player):
        self._turns.append(coord + (player,))
    
    def save_json(self, path):
        data = {'turns': self.turns, 'winner': self.winner}
        json.dump(data, open(path, 'w'))
    
    def reset(self):
        self._turns = []
        self._winner = None
