import tkinter as tk

from States.gameover import GameOverState


class PausedState(GameOverState):
    def __init__(self, window: tk.Tk):
        super().__init__(window, "Paused", include_resume=True)
