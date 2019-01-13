import numpy as np
from Tile import Tile

class PuzzleBoard:
    tiles = [0] *9
    winningState = [0] *9

    def __init__(self):
        for i in range(9):
            if i != 0:
                self.tiles[i] = Tile(i)
                self.winningState[i] = Tile(i)
            else:
                self.tiles[i] = None
                self.winningState[i] = None

        self.tiles = np.asarray(self.tiles).reshape(3, 3)
        self.resetPuzzle()
        self.winningState = np.asarray(self.winningState).reshape(3,3)
        self.getZeroLocation()
        print(self.getZeroLocation())

    def getState(self):
        return self.tiles

    def resetPuzzle(self):
        print("Resetting tiles!")
        temp = self.tiles.ravel()
        np.random.shuffle(temp)
        self.tiles = temp.reshape(3, 3)
        self.zero_location = self.getZeroLocation()
        print(self.getZeroLocation())

        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] != None:
                    print(self.tiles[i][j].getValue())
                else:
                    print(self.tiles[i][j])

    def getZeroLocation(self):
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] == None:
                    self.zero_location = {'col':i,'row':j}
        return self.zero_location

    def setZeroLocation(self, newLoc):
        self.zero_location = newLoc

    def moveLeft(self):
        print('left')
        tempLoc = self.getZeroLocation()
        if tempLoc['col'] != 0:
            print('moving left')
            leftTile = self.tiles[tempLoc['row']][tempLoc['col']-1]
            self.tiles[tempLoc['col']-1][tempLoc['row']] = None
            self.setZeroLocation({'col':tempLoc['col']-1,'row':tempLoc['row']})
            self.tiles[tempLoc['col']][tempLoc['row']] = leftTile
        else:
            print('cant move')
            print(self.getZeroLocation())
        return self.checkWin()

    def moveRight(self):
        print('right')
        tempLoc = self.getZeroLocation()
        if tempLoc['col'] != 2:
            print('moving right')
            rightTile = self.tiles[tempLoc['row']][tempLoc['col']+1]
            self.tiles[tempLoc['col']+1][tempLoc['row']] = None
            self.setZeroLocation({'col':tempLoc['col']+1,'row':tempLoc['row']})
            self.tiles[tempLoc['col']][tempLoc['row']] = rightTile
        else:
            print('cant move')
            print(self.getZeroLocation())
        return self.checkWin()

    def moveUp(self):
        print('up')
        tempLoc = self.getZeroLocation()
        if tempLoc['row'] != 0:
            print('moving up')
            aboveTile = self.tiles[tempLoc['row']-1][tempLoc['col']]
            self.tiles[tempLoc['col']][tempLoc['row']-1] = None
            self.setZeroLocation({'col':tempLoc['col'],'row':tempLoc['row']-1})
            self.tiles[tempLoc['col']][tempLoc['row']] = aboveTile
        else:
            print('cant move')
            print(self.getZeroLocation())
        return self.checkWin()

    def moveDown(self):
        print('down')
        tempLoc = self.getZeroLocation()
        if tempLoc['row'] != 2:
            print('moving down')
            belowTile = self.tiles[tempLoc['row']+1][tempLoc['col']]
            self.tiles[tempLoc['col']][tempLoc['row']+1] = None
            self.setZeroLocation({'col':tempLoc['col'],'row':tempLoc['row']+1})
            self.tiles[tempLoc['col']][tempLoc['row']] = belowTile
        else:
            print('cant move')
            print(self.getZeroLocation())
        return self.checkWin()

    def checkWin(self):
        if np.array_equal(self.tiles, self.winningState):
            print('You win')
            return True
