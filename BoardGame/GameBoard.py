import copy
import numpy as np


class GameBoard(object):
    def __init__(self, shape=(3, 3)):
        self._array = -np.ones(shape=shape, dtype=int)
    
    @property
    def array(self):
        return self._array
    
    @property
    def shape(self):
        return self._array.shape
    
    @property
    def m(self):
        return self.shape[0]
    
    @property
    def n(self):
        return self.shape[1]
    
    @property
    def is_empty(self):
        return np.all(self._array == -1)
    
    @property
    def is_full(self):
        return np.all(self._array != -1)
    
    @property
    def is_reflectional0(self):
        return np.all(self._array == self._array[::-1, :])
    
    @property
    def is_reflectional1(self):
        return np.all(self._array == self._array[:, ::-1])
    
    @property
    def is_rotational90(self):
        if self.shape[0] != self.shape[1]:
            return False
        else:
            r0 = self._array
            ind = True
            for i in range(1, 4):
                r = np.rot90(r0, k=i)
                ind = ind and np.all(r == r0)
            return ind
    
    @property
    def is_rotational180(self):
        r0 = self._array
        r = np.rot90(r0, k=2)
        return np.all(r == r0)
    
    @property
    def available_coords(self):
        self.all_available_coords
    
    @property
    def all_available_coords(self):
        return [(r, c) for r, c in zip(*np.where(self._array == -1))]
    
    @property
    def reduced_available_coords(self):
        all_coords = self.all_available_coords
        reduced_coords = []
        for coord in all_coords:
            duplicated = False
            if len(reduced_coords) == 0:
                reduced_coords.append(coord)
                continue
            # Reflective symmetry
            if self.is_reflectional0:
                if (self.m - 1 - coord[0], coord[1]) in reduced_coords:
                    duplicated = True
            if self.is_reflectional1:
                if (coord[0], self.n - 1 - coord[1]) in reduced_coords:
                    duplicated = True
            # Rotational symmetry
            if self.is_rotational180:
                if (self.m - 1 - coord[0], self.n - 1 - coord[1]) in reduced_coords:
                    duplicated = True
            if self.is_rotational90:
                if (coord[1], self.n - 1 - coord[0]) in reduced_coords:
                    duplicated = True
                if (self.m - 1 - coord[1], coord[0]) in reduced_coords:
                    duplicated = True
            if not duplicated:
                reduced_coords.append(coord)
        return reduced_coords
    
    def place_stone(self, row, col, player):
        self._array[row, col] = player
    
    def reset(self):
        self._array = -np.ones(shape=self.shape, dtype=int)
    
    def copy(self):
        return copy.deepcopy(self)
    
    def _get_lines_passing(self, row, col):
        board = self._array
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
        board = self._array
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
