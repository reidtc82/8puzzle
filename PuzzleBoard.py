import numpy as np
from Tile import Tile

class PuzzleBoard:
    tiles = [0] *9
    winningState = [0] *9

    def __init__(self):
        for i in range(9):
            if i != 0:
                self.tiles[i] = Tile(i)
                # self.winningState[i] = Tile(i)
            else:
                self.tiles[i] = None
                # self.winningState[i] = None

        self.winningState[0] = Tile(1)
        self.winningState[1] = Tile(8)
        self.winningState[2] = Tile(7)
        self.winningState[3] = Tile(2)
        self.winningState[4] = None
        self.winningState[5] = Tile(6)
        self.winningState[6] = Tile(3)
        self.winningState[7] = Tile(4)
        self.winningState[8] = Tile(5)

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
        self.printState(self.tiles)

    def printState(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] != None:
                    print(state[i][j].getValue())
                else:
                    print(state[i][j])

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
            leftTile = self.tiles[tempLoc['col']-1][tempLoc['row']]
            self.tiles[tempLoc['col']-1][tempLoc['row']] = None
            self.setZeroLocation({'col':tempLoc['col']-1,'row':tempLoc['row']})
            self.tiles[tempLoc['col']][tempLoc['row']] = leftTile
        else:
            print('cant move')
            print(self.getZeroLocation())
        # self.printState(self.tiles)
        if self.checkWin():
            print('Youwin!')

    def moveRight(self):
        print('right')
        tempLoc = self.getZeroLocation()
        if tempLoc['col'] != 2:
            print('moving right')
            rightTile = self.tiles[tempLoc['col']+1][tempLoc['row']]
            self.tiles[tempLoc['col']+1][tempLoc['row']] = None
            self.setZeroLocation({'col':tempLoc['col']+1,'row':tempLoc['row']})
            self.tiles[tempLoc['col']][tempLoc['row']] = rightTile
        else:
            print('cant move')
            print(self.getZeroLocation())
        # self.printState(self.tiles)
        if self.checkWin():
            print('Youwin!')

    def moveUp(self):
        print('up')
        tempLoc = self.getZeroLocation()
        if tempLoc['row'] != 0:
            print('moving up')
            aboveTile = self.tiles[tempLoc['col']][tempLoc['row']-1]
            self.tiles[tempLoc['col']][tempLoc['row']-1] = None
            self.setZeroLocation({'col':tempLoc['col'],'row':tempLoc['row']-1})
            self.tiles[tempLoc['col']][tempLoc['row']] = aboveTile
        else:
            print('cant move')
            print(self.getZeroLocation())
        # self.printState(self.tiles)
        if self.checkWin():
            print('Youwin!')

    def moveDown(self):
        print('down')
        tempLoc = self.getZeroLocation()
        if tempLoc['row'] != 2:
            print('moving down')
            belowTile = self.tiles[tempLoc['col']][tempLoc['row']+1]
            self.tiles[tempLoc['col']][tempLoc['row']+1] = None
            self.setZeroLocation({'col':tempLoc['col'],'row':tempLoc['row']+1})
            self.tiles[tempLoc['col']][tempLoc['row']] = belowTile
        else:
            print('cant move')
            print(self.getZeroLocation())
        # self.printState(self.tiles)
        if self.checkWin():
            print('Youwin!')

    def checkWin(self):
        print('current state')
        self.printState(self.tiles)
        print('\n')
        print('winning state')
        self.printState(self.winningState)
        youWin = True
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] and self.winningState[i][j]:
                    if self.tiles[i][j].getValue != self.winningState[i][j].getValue:
                        youWin = False
        return youWin
