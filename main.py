from tkinter import Tk, Label, Button
from PuzzleBoard import PuzzleBoard
import numpy as np

class Main:
    def __init__(self, master):
        self.master = master
        master.title("8 Puzzle")
        master.geometry('640x480')

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Reset Puzzle", command=self.resetPuzzle)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.board = PuzzleBoard()

    def resetPuzzle(self):
        self.board.resetState()
        currentState = np.asarray(self.board.getState())
        print(currentState)

root = Tk()
mainPanel = Main(root)
root.mainloop()
