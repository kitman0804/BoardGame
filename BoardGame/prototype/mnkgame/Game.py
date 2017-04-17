from copy import deepcopy
from .Core import Core
from ..Recorder import Recorder
from .players.Player import Player
from .players.Human import Human


class Game(object):
    def __init__(self, m, n, k, player_cycle=(0, 1)):
        self._core = Core(m=m, n=n, k=k, player_cycle=player_cycle)
        self._players = [
            Human(name='P0', stone=0),
            Human(name='P1', stone=1)
        ]
        self._recorder = Recorder()
    
    @property
    def core(self):
        return self._core
    
    @property
    def gameboard(self):
        return self._core.gameboard
    
    @property
    def current_player(self):
        return self._core.current_player
    
    @property
    def winner(self):
        return self._core.winner
    
    @property
    def is_ended(self):
        return self._core.is_ended
    
    @property
    def players(self):
        return self._players
    
    @property
    def player0(self):
        return self._players[0]
    
    @player0.setter
    def player0(self, x):
        if isinstance(x, Player):
            x.stone = 0
            self._players[0] = x
        else:
            raise TypeError('Unqualified player.')
    
    @property
    def player1(self):
        return self._players[1]
    
    @player1.setter
    def player1(self, x):
        if isinstance(x, Player):
            x.stone = 1
            self._players[1] = x
        else:
            raise TypeError('Unqualified player.')
    
    def place_stone(self, row, col, stone):
        self._core.place_stone(row=row, col=col, stone=stone)
    
    def next_turn(self):
        coord = None
        while coord is None:
            player = self._players[self._core.current_player]
            gameboard = self._core.gameboard
            available_coords = gameboard.available_coords
            coord = player.decide(game=self.core)
            stone = player.stone
            if coord == 'pause':
                print('The game is paused.')
                return None
            elif coord not in available_coords:
                print('Invalid move. Only the following slots were avaiable:')
                print('  ', list(available_coords))
            else:
                self._core.place_stone(*coord, stone=stone)
                self._recorder.record(coord=coord, player=stone)
        winner = self._core.winner
        if winner is None:
            self.next_turn()
        else:
            self._recorder.winner = winner
    
    def start(self, player0=None, player1=None):
        if player0 is not None:
            self.player0 = player0
        if player1 is not None:
            self.player1 = player1
        # Start game
        self.next_turn()
        # End game
        gameboard = self._core.gameboard
        winner = self._players[self._core.winner]
        if winner == -1:
            msg = 'Draw! What a game!'
        else:
            msg = 'Congratulations! {:} won!'.format(winner.name)
        print(gameboard)
        print(msg)
    
    def reset(self):
        self._core.reset()
        self._recorder.reset()
    
    def restart(self):
        self.reset()
        self.start()
    
    def copy(self):
        return deepcopy(self)
