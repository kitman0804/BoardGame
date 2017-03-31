import numpy as np
from ..BoardGame import BoardGame
from .GameBoard import GameBoard
from ..players import Player, Human


class ConnectFour(BoardGame):
    category='m,n,k-game (constrainted)'
    m, n, k = 6, 7, 4
    n_players = 2
    
    def __init__(self):
        super().__init__()
        self._gameboard = GameBoard()
        self._turn = 0
        self._winner = None
    
    @property
    def player0(self):
        return self._player0
    
    @player0.setter
    def player0(self, x):
        if isinstance(x, Player):
            self._player0 = x
    
    @property
    def player1(self):
        return self._player1_selector
    
    @player1.setter
    def player1(self, x):
        if isinstance(x, Player):
            self._player1 = x
    
    @property
    def players(self):
        return (self._player0, self._player1)
        @property
        def turn_player(self):
            return self._turn % 2
    
    @property
    def turn_player(self):
        return self._turn % 2
    
    def find_winner(self, row=None, col=None):
        who = self._turn % 2
        # Check if someone has won
        for l in self._gameboard.get_lines(row=row, col=col):
            if len(l) < self.k:
                pass
            else:
                count = 0
                for x in l:
                    count += 1 if x == who else -count
                    if count == self.k:
                        return who
                    else:
                        pass
        # If no one won, check if it is a draw game.
        if self._gameboard.is_full:
            return -1
        else:
            return None
    
    def move(self, row, col, player):
        self._gameboard.put(row=row, col=col, player=player)
        self._winner = self.find_winner(row=row, col=col)
        self._turn += 1
    
    def start(self, player0=Human(name='Player 0'), player1=Human(name='Player 1')):
        if not (isinstance(player0, Player) and isinstance(player1, Player)):
            raise ValueError('player0 and player1 must be a Player.')
        else:
            player0.player = 0
            player1.player = 1
            self._player0 = player0
            self._player1 = player1
            while self._winner is None:
                available_moves = self._gameboard.available_moves
                move = None
                while move not in available_moves:
                    move = self.players[self._turn % 2].decide(game=self)
                    if move == 'pause':
                        print('The game is paused.')
                        return None
                    elif move not in available_moves:
                        print('Invalid move. Only the following slots were avaiable:')
                        print('  ', list(available_moves.keys()))
                    else:
                        pass
                self.move(*move, player=self._turn % 2)
            # Print result
            if self._winner == -1:
                msg = 'Draw! What a game!'
            else:
                msg = 'Congratulations! {:} won!'.format(self.players[self._winner].name)
            print(self._gameboard.gameboard)
            print(msg)
    
    def reset(self):
        self._gameboard.reset()
        self._turn = 0
        self._winner = None
    
    def restart(self):
        self.reset()
        self.start(player0=self._player0, player1=self._player1)
