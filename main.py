import sys
if sys.version_info[0] == 3:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
else:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter

# from tkinter import Tk, Label, Button, Canvas

from PuzzleBoard import PuzzleBoard
from State import State
import numpy as np

class Main:
    def __init__(self, master):
        self.canvas_width = 300
        self.canvas_height = 300
        self.rectangles = [0] *8
        self.texts = [0] *8

        self.board = PuzzleBoard()

        self.master = master
        master.title("8 Puzzle")
        master.geometry('640x480')

        self.label = Label(master, text="This is 8 Puzzle")
        self.label.pack()

        self.score = Label(master, text=self.board.getScore())
        self.score.pack()

        self.canvasSpace = Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvasSpace.pack()

        self.canvasSpace.create_rectangle(0, 0, 300, 300, fill="#696969")
        self.drawBoard(self.canvasSpace)

        self.resetPuzzle_button = Button(master, text="Reset Puzzle", command=self.newPuzzle)
        self.resetPuzzle_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.up_button = Button(master, text="Up", command=self.moveUp)
        self.up_button.pack()

        self.down_button = Button(master, text="Down", command=self.moveDown)
        self.down_button.pack()

        self.left_button = Button(master, text="Left", command=self.moveLeft)
        self.left_button.pack()

        self.right_button = Button(master, text="Right", command=self.moveRight)
        self.right_button.pack()

    def moveRight(self):
        self.board.moveRight()
        self.score.config(text=self.board.getScore())
        self.drawBoard(self.canvasSpace)

    def moveLeft(self):
        self.board.moveLeft()
        self.score.config(text=self.board.getScore())
        self.drawBoard(self.canvasSpace)

    def moveDown(self):
        self.board.moveDown()
        self.score.config(text=self.board.getScore())
        self.drawBoard(self.canvasSpace)

    def moveUp(self):
        self.board.moveUp()
        self.score.config(text=self.board.getScore())
        self.drawBoard(self.canvasSpace)

    def newPuzzle(self):
        print('hello')
        self.board.resetPuzzle()
        self.board.resetScore()
        self.score.config(text=self.board.getScore())
        self.drawBoard(self.canvasSpace)

    def drawBoard(self, canvas):
        for rec in self.rectangles:
            canvas.delete(rec)

        for txt in self.texts:
            canvas.delete(txt)

        currentState = self.board.getState()
        for i in range(3):
            for j in range(3):
                if currentState[i][j] != 0:
                    origin_X = 100*i
                    origin_Y = 100*j
                    final_X = origin_X+100
                    final_Y = origin_Y+100
                    self.rectangles.append(canvas.create_rectangle(origin_X, origin_Y, final_X, final_Y, fill="#DCDCDC"))
                    self.texts.append(canvas.create_text(origin_X+50,origin_Y+50,text=currentState[i][j]))

root = Tk()
mainPanel = Main(root)
root.mainloop()
