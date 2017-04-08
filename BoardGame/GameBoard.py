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
    
    def is_equal_ref(self, axis=0):
        b_0 = self._array
        if axis == 0:
            b_r = self._array[::-1, :]
            return np.all(b_0 == b_r)
        elif axis == 1:
            b_r = self._array[:, ::-1]
            return np.all(b_0 == b_r)
        elif axis == 'd':
            if self.shape[0] != self.shape[1]:
                return False
            else:
                b_r = np.transpose(self._array)
                return np.all(b_0 == b_r)
        elif axis == 'ad':
            if self.shape[0] != self.shape[1]:
                return False
            else:
                b_r = np.transpose(self._array[:, ::-1])[:, ::-1]
                return np.all(b_0 == b_r)
        else:
            raise ValueError('Invalid axis. (0, 1, \'d\', \'ad\')')
    
    def is_equal_rot(self, angle=90):
        if self.shape[0] != self.shape[1]:
            return False
        elif angle in (90, 180, 270):
            b_0 = self._array
            b_r = np.rot90(self._array, k=angle // 90)
            return np.all(b_0 == b_r)
        else:
            raise ValueError('Invalid angle. (90, 180, 270)')
    
    @property
    def all_available_coords(self):
        return [(r, c) for r, c in zip(*np.where(self._array == -1))]
    
    @property
    def reduced_available_coords(self):
        return list(self.equivalent_coords.keys())
    
    @property
    def equivalent_coords(self):
        all_coords = self.all_available_coords
        eq_coords = dict()
        for coord in all_coords:
            exist_equivalent = False
            if len(eq_coords) == 0:
                eq_coords.update({coord: [coord]})
                continue
            # Reflective symmetry
            if self.is_equal_ref(axis=0):
                eq_coord= (self.m - 1 - coord[0], coord[1])
                if eq_coord in eq_coords.keys():
                    exist_equivalent = True
                    eq_coords.get(eq_coord).append(coord)
            if self.is_equal_ref(axis=1):
                eq_coord= (coord[0], self.n - 1 - coord[1])
                if eq_coord in eq_coords.keys():
                    exist_equivalent = True
                    eq_coords.get(eq_coord).append(coord)
            if self.is_equal_ref(axis='d'):
                eq_coord= (coord[1], coord[0])
                if eq_coord in eq_coords.keys():
                    exist_equivalent = True
                    eq_coords.get(eq_coord).append(coord)
            if self.is_equal_ref(axis='ad'):
                eq_coord= (self.n - 1 - coord[1], self.m - 1 - coord[0])
                if eq_coord in eq_coords.keys():
                    exist_equivalent = True
                    eq_coords.get(eq_coord).append(coord)
            # Rotational symmetry
            if (self.is_equal_rot(angle=90) and
                self.is_equal_rot(angle=180) and
                self.is_equal_rot(angle=270)):
                eq_coord= (coord[1], self.n - 1 - coord[0])
                if eq_coord in eq_coords.keys():
                    exist_equivalent = True
                    eq_coords.get(eq_coord).append(coord)
                eq_coord= (self.m - 1 - coord[1], coord[0])
                if eq_coord in eq_coords.keys():
                    exist_equivalent = True
                    eq_coords.get(eq_coord).append(coord)
                eq_coord= (self.m - 1 - coord[0], self.n - 1 - coord[1])
                if eq_coord in eq_coords.keys():
                    exist_equivalent = True
                    eq_coords.get(eq_coord).append(coord)
            elif self.is_equal_rot(angle=180):
                eq_coord= (self.m - 1 - coord[0], self.n - 1 - coord[1])
                if eq_coord in eq_coords.keys():
                    exist_equivalent = True
                    eq_coords.get(eq_coord).append(coord)
            if not exist_equivalent:
                eq_coords.update({coord: [coord]})
        eq_coords = {k: list(set(x)) for k, x in eq_coords.items()}
        return eq_coords
    
    def place_stone(self, row, col, player):
        self._array[row, col] = player
    
    def reset(self):
        self._array = -np.ones(shape=self.shape, dtype=int)
    
    def copy(self):
        return copy.deepcopy(self)
    
    def get_lines(self, row=None, col=None):
        board_array = self.array
        n_row, n_col = board_array.shape
        if row is None or col is None:
            # All horizontal lines
            for i in range(n_row):
                yield board_array[i, :]
            # All vertical lines
            for j in range(n_col):
                yield board_array[:, j]
            # All diagonal & anti-diagonal lines
            for i in range(-n_row + 1, n_col):
                yield np.diagonal(board_array, offset=i)
                yield np.diagonal(board_array[:, ::-1], offset=i)
        else:
            # Horizontal line (-) passing (row, col)
            yield board_array[row, :]
            # Vertical line (|) passing (row, col)
            yield board_array[:, col]
            # Diagonal line (\) passing (row, col)
            yield np.diagonal(board_array, offset=col - row)
            # Anti-diagonal line (/) passing (row, col)
            yield np.diagonal(board_array[:, ::-1], offset=n_col - col - 1 - row)
