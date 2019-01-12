import numpy as np
import Tile as tile

class PuzzleBoard:
    def __init__(self):
        self.tiles = np.arange(9).reshape(3, 3)

    def getState(self):
        return self.tiles

    def resetState(self):
        print("Resetting tiles!")
        self.tiles = np.arange(9).reshape(3, 3)
        np.random.shuffle(self.tiles.ravel())
        self.tiles.reshape(3,3)
