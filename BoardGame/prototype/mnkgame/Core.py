from .GameBoard import GameBoard


class Core(object):
    def __init__(self, m=3, n=3, k=3, player_cycle=(0, 1),
                 gameboard=None, turn=None, winner=None):
        self._k = k
        self._player_cycle = player_cycle
        if gameboard is None:
            self._gameboard = GameBoard(shape=(m, n))
        elif isinstance(gameboard, GameBoard):
            self._gameboard = gameboard.copy()
        else:
            raise TypeError('Invalid gameboard.')
        self._turn = 0 if turn is None else turn
        self._winner = None if winner is None else winner
    
    @property
    def m(self):
        return self._gameboard.m
    
    @property
    def n(self):
        return self._gameboard.n
    
    @property
    def k(self):
        return self._k
    
    @property
    def player_cycle(self):
        return self._player_cycle
    
    @property
    def gameboard(self):
        return self._gameboard
    
    @gameboard.setter
    def gameboard(self, x):
        if isinstance(x, GameBoard):
            self._gameboard = x
        else:
            raise TypeError('Invalid GameBoard.')
    
    @property
    def turn(self):
        return self._turn
    
    @turn.setter
    def turn(self, x):
        if isinstance(x, int):
            self._turn = x
        else:
            raise TypeError('Turn must be an integer.')
    
    @property
    def current_player(self):
        if self._winner is None:
            cycle = self._player_cycle
            return cycle[self._turn % len(cycle)]
        else:
            return None
    
    @property
    def winner(self):
        return self._winner
    
    @winner.setter
    def winner(self, x):
        if x in [None, -1] or x in self._player_cycle:
            self._winner = x
        else:
            raise ValueError('No such player.')
    
    @property
    def is_ended(self):
        return self._winner is not None
    
    def place_stone(self, row, col, stone):
        if (row not in range(self.m) and col not in range(self.n)):
            raise IndexError('Invalid row/col.')
        if stone not in self._player_cycle:
            raise ValueError('Invalid stone.')
        else:
            self._gameboard.place_stone(row=row, col=col, stone=stone)
            self._winner = self.find_winner(row=row, col=col)
            self._turn += 1
    
    def find_winner(self, row, col):
        p = self._gameboard.array[row, col]
        if p == -1:
            return None
        else:
            lines = self._gameboard.get_lines(row=row, col=col)
            for l in lines:
                if len(l) < self._k:
                    continue
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
    
    def reset(self):
        self._gameboard.reset()
        self._turn = 0
        self._winner = None
    
    def copy(self):
        clone = type(self)(
            k=self._k,
            player_cycle=self._player_cycle,
            gameboard=self._gameboard,
            turn=self._turn,
            winner=self._winner
        )
        return clone
