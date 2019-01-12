from tkinter import Tk, Label, Button
from PuzzleBoard import PuzzleBoard
import numpy as np

class Main:
    def __init__(self, master):
        self.board = PuzzleBoard()

        self.master = master
        master.title("8 Puzzle")
        master.geometry('640x480')

        self.label = Label(master, text="This is 8 Puzzle")
        self.label.pack()

        self.resetPuzzle_button = Button(master, text="Reset Puzzle", command=self.board.resetPuzzle)
        self.resetPuzzle_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.up_button = Button(master, text="Up", command=self.board.moveUp)
        self.up_button.pack()

        self.down_button = Button(master, text="Down", command=self.board.moveDown)
        self.down_button.pack()

        self.left_button = Button(master, text="Left", command=self.board.moveLeft)
        self.left_button.pack()

        self.right_button = Button(master, text="Right", command=self.board.moveRight)
        self.right_button.pack()


root = Tk()
mainPanel = Main(root)
root.mainloop()
