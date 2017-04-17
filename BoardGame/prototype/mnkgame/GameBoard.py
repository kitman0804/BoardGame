import copy
import numpy as np


class GameBoard(object):
    def __init__(self, shape=(3, 3)):
        self._array = -np.ones(shape=shape, dtype=int)
    
    def __str__(self):
        return str(self._array)
    
    @property
    def array(self):
        return self._array
    
    @array.setter
    def array(self, x):
        if isinstance(x, np.ndarray):
            if len(x.shape) == 1:
                self._array = x
            else:
                raise TypeError('x must be a 2D numpy.ndarray.')
        else:
            raise TypeError('x must be a 2D numpy.ndarray.')
    
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
    def available_coords(self):
        return [(r, c) for r, c in zip(*np.where(self._array == -1))]
    
    @property
    def equivalent_coords_dict(self):
        b_0 = self._array
        m, n = b_0.shape
        coords_dict = dict()
        for coord in self.available_coords:
            if len(coords_dict) == 0:
                coords_dict.update({coord: {coord}})
            else:
                found_equivalent = False
                # Reflective symmetry
                # left-right
                b_r = b_0[::-1, :]
                if np.all(b_0 == b_r):
                    eq_coord = (m - 1 - coord[0], coord[1])
                    if eq_coord in coords_dict.keys():
                        found_equivalent = True
                        coords_dict[eq_coord].update([coord])
                # top-bottom
                b_r = b_0[:, ::-1]
                if np.all(b_0 == b_r):
                    eq_coord = (coord[0], n - 1 - coord[1])
                    if eq_coord in coords_dict.keys():
                        found_equivalent = True
                        coords_dict[eq_coord].update([coord])
                if m == n:
                    # Diagonal
                    b_r = np.transpose(b_0)
                    if np.all(b_0 == b_r):
                        eq_coord = (coord[1], coord[0])
                        if eq_coord in coords_dict.keys():
                            found_equivalent = True
                            coords_dict[eq_coord].update([coord])
                    # Anti-diagonal
                    b_r = np.transpose(b_0[:, ::-1])[:, ::-1]
                    if np.all(b_0 == b_r):
                        eq_coord = (n - 1 - coord[1], m - 1 - coord[0])
                        if eq_coord in coords_dict.keys():
                            found_equivalent = True
                            coords_dict[eq_coord].update([coord])
                # Rotational symmetry
                if m == n:
                    # 90 degree
                    if (np.all(b_0 == np.rot90(b_0, k=1)) and
                        np.all(b_0 == np.rot90(b_0, k=2)) and
                        np.all(b_0 == np.rot90(b_0, k=3))):
                        eq_coord = (coord[1], n - 1 - coord[0])
                        if eq_coord in coords_dict.keys():
                            found_equivalent = True
                            coords_dict[eq_coord].update([coord])
                        eq_coord = (m - 1 - coord[1], coord[0])
                        if eq_coord in coords_dict.keys():
                            found_equivalent = True
                            coords_dict[eq_coord].update([coord])
                        eq_coord = (m - 1 - coord[0], n - 1 - coord[1])
                        if eq_coord in coords_dict.keys():
                            found_equivalent = True
                            coords_dict[eq_coord].update([coord])
                else:
                    # 180 degree
                    if np.all(b_0 == np.rot90(b_0, k=2)):
                        eq_coord = (m - 1 - coord[0], n - 1 - coord[1])
                        if eq_coord in coords_dict.keys():
                            found_equivalent = True
                            coords_dict[eq_coord].update([coord])
                if not found_equivalent:
                    coords_dict.update({coord: {coord}})
        # Uniqueness
        coords_dict = {k: list(x) for k, x in coords_dict.items()}
        # Return dictionary
        return coords_dict
    
    def place_stone(self, row, col, stone):
        self._array[row, col] = stone
    
    def reset(self):
        self._array = -np.ones(shape=self.shape, dtype=int)
    
    def copy(self):
        return copy.deepcopy(self)
    
    def get_lines(self, row=None, col=None):
        board_array = self.array
        m, n = board_array.shape
        if row is None or col is None:
            # All horizontal lines
            for i in range(m):
                yield board_array[i, :]
            # All vertical lines
            for j in range(n):
                yield board_array[:, j]
            # All diagonal & anti-diagonal lines
            for i in range(-m + 1, n):
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
            yield np.diagonal(board_array[:, ::-1], offset=n - 1 - col - row)
