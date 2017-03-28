class BoardGame(object):
    def __init__(self, category='', n_players=None):
        self._category = ''
        self._n_players = n_players
    
    @property
    def category(self):
        return self._category
    
    @property
    def n_players(self):
        return self._n_players
