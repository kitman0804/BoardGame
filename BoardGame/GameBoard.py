import copy
import numpy as np


class GameBoard(object):
    def __init__(self, shape=(3, 3)):
        self._gameboard = -np.ones(shape=shape, dtype=int)
    
    @property
    def gameboard(self):
        return self._gameboard
    
    @property
    def shape(self):
        return self._gameboard.shape
    
    @property
    def is_empty(self):
        return np.sum(self._gameboard != -1) == 0
    
    @property
    def is_full(self):
        return np.sum(self._gameboard == -1) == 0
    
    @property
    def is_symmetric(self, axis=0):
        if axis == 0:
            return np.sum(self._gameboard != self._gameboard[::-1, :]) == 0
        elif axis == 1:
            return np.sum(self._gameboard != self._gameboard[:, ::-1]) == 0
        elif axis == (0, 1):
            ax0 = np.sum(self._gameboard != self._gameboard[::-1, :]) == 0
            ax1 = np.sum(self._gameboard != self._gameboard[:, ::-1]) == 0
            return ax0 and ax1
        else:
            raise ValueError('Invalid axis.')
    
    @property
    def is_rotational_summetric(self):
        pass
    
    def put(self, row, col, player):
        self._gameboard[row, col] = player
    
    def clean(self):
        self._gameboard = -np.ones(shape=self.shape, dtype=int)
    
    def reset(self):
        self._gameboard = -np.ones(shape=self.shape, dtype=int)
    
    def copy(self):
        return copy.deepcopy(self)
    
    def _get_lines_passing(self, row, col):
        board = self._gameboard
        n_row, n_col = board.shape
        # Flatten the board into 1-D
        b_flat = board.reshape(-1)
        # Horizontal line (-) passing (row, col)
        h_line = b_flat[row * n_col:row * n_col + n_col]
        yield h_line
        # Vertical line (|) passing (row, col)
        v_line = b_flat[col::n_col]
        yield v_line
        # Anti-diagonal line (/) passing (row, col)
        ad_start = max(col - row, (row - col) * n_col)
        ad_end = min(n_row, row + n_col - col) * n_col
        ad_line = b_flat[ad_start:ad_end + 1:n_col + 1]
        yield ad_line
        # Diagonal line (\) passing (row, col)
        d_start = max(row + col, (row - (n_col - col - 1)) * n_col + n_col - 1)
        d_end = min(n_row, row + col) * n_col
        d_line = b_flat[d_start:d_end + 1:n_col - 1]
        yield d_line
    
    def _get_all_lines(self):
        board = self._gameboard
        n_row, n_col = board.shape
        # All horizontal lines
        for i in range(n_row):
            yield board[i, :]
        # All vertical lines
        for j in range(n_col):
            yield board[:, j]
        # All diagonal and anti-diagonal lines
        for i in range(n_row):
            yield board[range(i, min(n_row, n_row + i)), range(0, min(n_row, n_row - i))]
            yield board[:, ::-1][range(i, min(n_row, n_row + i)), range(0, min(n_row, n_row - i))]
        for j in range(1, n_col):
            yield board[range(0, min(n_col, n_col - j)), range(j, min(n_col, n_col + j))]
            yield board[:, ::-1][range(0, min(n_col, n_col - j)), range(j, min(n_col, n_col + j))]
    
    def get_lines(self, row=None, col=None):
        if row is None or col is None:
            return self._get_all_lines()
        else:
            return self._get_lines_passing(row=row, col=col)
    
    @property
    def available_moves(self):
        return [(r, c) for r, c in zip(*np.where(self._gameboard == -1))]
