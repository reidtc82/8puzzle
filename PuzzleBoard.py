import numpy as np

class PuzzleBoard:
    def __init__(self,tiles):
        self.tiles = tiles

    def getState(self):
        return self.tiles

    def resetState(self):
        print("Resetting tiles!")
        self.tiles = np.arange(9).reshape(3, 3)
        np.random.shuffle(self.tiles.ravel())
        self.tiles.reshape(3,3)
