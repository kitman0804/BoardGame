from ..prototype.mnkgame.GameBoard import GameBoard


class GameBoard(GameBoard):
    def __init__(self):
        super().__init__(shape=(6, 7))
    
    @property
    def available_coords(self):
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
