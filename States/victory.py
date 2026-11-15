import tkinter as tk

from States.gameover import GameOverState


class VictoryState(GameOverState):
    def __init__(self, window: tk.Tk):
        super().__init__(window, "Victory!")
