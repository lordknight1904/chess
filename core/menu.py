import tkinter as tk
from core.game import Game
LARGE_FONT= ("Verdana", 12)


class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label2 = tk.Label(self, text="Simple Chess Game").grid(row=0, column=0)
        label2.pack()

        choices = {'Hard', 'Normal', 'Easy'}
        # self.difficulty.set('Easy') # set the default option

        difficulty_menu = tk.OptionMenu(self, controller.difficulty, *choices, command=controller.select_difficulty)
        tk.Label(self, text="Difficulty").grid(row=1, column=0)
        difficulty_menu.grid(row=1, column=1)
        difficulty_menu.pack()

        button1 = tk.Button(self, text="Start", command=lambda: controller.show_frame(Game))
        button1.pack()
        button2 = tk.Button(self, text="Quit", command=parent.destroy)
        button2.pack()

