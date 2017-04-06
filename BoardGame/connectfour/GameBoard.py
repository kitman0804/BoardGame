from ..GameBoard import GameBoard


class GameBoard(GameBoard):
    def __init__(self):
        super().__init__(shape=(6, 7))
    
    @property
    def all_available_coords(self):
        coords = []
        n_row, n_col = self._array.shape
        for c in range(n_col):
            for r in range(n_row):
                if self._array[r, c] == -1:
                    coords.append((r, c))
                    break
                else:
                    pass
        return coords
    
    @property
    def reduced_available_coords(self):
        all_coords = self.all_available_coords
        reduced_coords = []
        for coord in all_coords:
            duplicated = False
            if len(reduced_coords) == 0:
                reduced_coords.append(coord)
                continue
            # Reflective symmetry (Left-Right)
            if self.is_reflectional1:
                if (coord[0], self.n - 1 - coord[1]) in reduced_coords:
                    duplicated = True
            if not duplicated:
                reduced_coords.append(coord)
        return reduced_coords
