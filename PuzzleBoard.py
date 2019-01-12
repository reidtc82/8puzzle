import numpy as np
from Tile import Tile

class PuzzleBoard:
    tiles = [0] *9
    winningState = [0] *9

    def __init__(self):
        for i in range(9):
            self.tiles[i] = Tile(i)
            self.winningState[i] = Tile(i)

        self.tiles = np.asarray(self.tiles).reshape(3, 3)
        self.winningState = np.asarray(self.winningState).reshape(3,3)

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

    def moveUp(self):
        print('up')
        return self.checkWin()

    def moveDown(self):
        print('down')
        return self.checkWin()

    def moveLeft(self):
        print('left')
        return self.checkWin()

    def moveRight(self):
        print('right')
        return self.checkWin()

    def checkWin(self):
        return np.array_equal(self.tiles, self.winningState)
