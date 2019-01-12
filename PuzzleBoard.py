import numpy as np
from Tile import Tile

class PuzzleBoard:
    tiles = [0] *9
    def __init__(self):
        for i in range(9):
            self.tiles[i] = Tile(i)
        self.tiles = np.asarray(self.tiles).reshape(3, 3)

    def getState(self):
        return self.tiles

    def resetPuzzle(self):
        print("Resetting tiles!")
        temp = self.tiles.ravel()
        np.random.shuffle(temp)
        self.tiles = temp.reshape(3, 3)

        for i in range(3):
            for j in range(3):
                print(self.tiles[i][j].getValue())
