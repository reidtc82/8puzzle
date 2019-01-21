import numpy as np
from Tile import Tile
from State import State

class PuzzleBoard:
    tiles = [0] *9
    winningState = [0] *9
    score = 0

    def __init__(self):
        for i in range(9):
            self.tiles[i] = i

        self.easyStart = State([[1,8,7],[3,6,0],[4,2,5]],0,[])
        self.medStart = State([[2,0,7],[8,4,6],[1,3,5]],0,[])
        self.hardStart = State([[5,4,3],[6,0,2],[7,8,1]],0,[])
        self.winningState = State([[1,8,7],[2,0,6],[3,4,5]],0,[])

        # self.winningState[0] = 1
        # self.winningState[1] = 8
        # self.winningState[2] = 7
        # self.winningState[3] = 2
        # self.winningState[4] = 0
        # self.winningState[5] = 6
        # self.winningState[6] = 3
        # self.winningState[7] = 4
        # self.winningState[8] = 5

        self.tiles = np.asarray(self.tiles).reshape(3, 3)
        self.resetPuzzle()
        # self.winningState = np.asarray(self.winningState).reshape(3,3)
        self.getZeroLocation()
        print(self.getZeroLocation())

    def getScore(self):
        return self.score

    def getState(self):
        return self.tiles

    def resetPuzzle(self):
        print("Resetting tiles!")
        temp = self.tiles.ravel()
        np.random.shuffle(temp)
        self.tiles = temp.reshape(3, 3)
        self.zero_location = self.getZeroLocation()
        print(self.getZeroLocation())
        print(self.tiles)

    def resetScore(self):
        self.score = 0

    def getZeroLocation(self):
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] == 0:
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
            self.score += leftTile
            self.tiles[tempLoc['col']-1][tempLoc['row']] = 0
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
            self.score += rightTile
            self.tiles[tempLoc['col']+1][tempLoc['row']] = 0
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
            self.score += aboveTile
            self.tiles[tempLoc['col']][tempLoc['row']-1] = 0
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
            self.score += belowTile
            self.tiles[tempLoc['col']][tempLoc['row']+1] = 0
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
        print(self.tiles)
        print('\n')
        print('winning state')
        print(self.winningState.getState())
        print('\n')
        print(self.getScore())
        # print(np.allclose(self.tiles,self.tiles))
        return np.allclose(self.tiles, self.winningState.getState())
