from copy import deepcopy
from .GameBoard import GameBoard
from ..Recorder import Recorder
from .players.Player import Player
from .players.Human import Human


class Game(object):
    n_player = 2
    
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k
        self._gameboard = GameBoard(shape=(m, n))
        self._players = [
            Human(name='P0', stone=0),
            Human(name='P1', stone=1)
        ]
        self._recorder = Recorder()
        self._turn = 0
        self._winner = None
    
    @property
    def gameboard(self):
        return self._gameboard
    
    @property
    def player0(self):
        return self._players[0]
    
    @player0.setter
    def player0(self, x):
        if isinstance(x, Player):
            x.stone = 0
            self._players[0] = x
        else:
            raise TypeError('x is not a qualified player.')
    
    @property
    def player1(self):
        return self._players[1]
    
    @player1.setter
    def player1(self, x):
        if isinstance(x, Player):
            x.stone = 1
            self._players[1] = x
        else:
            raise TypeError('x is not a qualified player.')
    
    @property
    def players(self):
        return self._players
    
    @property
    def current_player(self):
        return self._turn % self.n_player
    
    @property
    def winner(self):
        return self._winner
    
    @property
    def is_ended(self):
        return self._winner is not None
    
    def find_winner(self, row, col):
        p = self._gameboard.array[row, col]
        if p == -1:
            return None
        else:
            lines = self._gameboard.get_lines(row=row, col=col)
            for l in lines:
                if len(l) < self.k:
                    pass
                else:
                    count = 0
                    for x in l:
                        if x == p:
                            count += 1
                            if count == self.k:
                                return p
                        else:
                            count = 0
            # If no one won, check if it is a draw game.
            if self._gameboard.is_full:
                return -1
            else:
                return None
    
    def place_stone(self, row, col, stone):
        self._gameboard.place_stone(row=row, col=col, stone=stone)
        self._winner = self.find_winner(row=row, col=col)
        self._turn += 1
    
    def next_turn(self):
        coord = None
        while coord is None:
            available_coords = self._gameboard.available_coords
            current_player = self._players[self.current_player]
            coord = current_player.decide(game=self)
            stone = current_player.stone
            if coord == 'pause':
                print('The game is paused.')
                return None
            elif coord not in available_coords:
                print('Invalid move. Only the following slots were avaiable:')
                print('  ', list(available_coords))
            else:
                self.place_stone(*coord, stone=stone)
                self._recorder.record(coord=coord, player=stone)
        if self._winner is None:
            self.next_turn()
            pass
    
    def start(self, player0=None, player1=None):
        if player0 is not None:
            self.player0 = player0
        if player1 is not None:
            self.player1 = player1
        # Start game
        self.next_turn()
        # End game
        self._recorder.winner = self._winner
        if self._winner == -1:
            msg = 'Draw! What a game!'
        else:
            msg = 'Congratulations! {:} won!'.format(self._players[self._winner].name)
        print(self._gameboard.array)
        print(msg)
    
    def reset(self):
        self._gameboard.reset()
        self._recorder.reset()
        self._turn = 0
        self._winner = None
    
    def restart(self):
        self.reset()
        self.start()
    
    def copy(self):
        return deepcopy(self)
