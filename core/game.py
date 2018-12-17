from core.menu import Menu
import tkinter as tk
LARGE_FONT= ("Verdana", 12)


class Game(tk.Frame):
    pieces = {}
    selected = None
    selected_piece = None
    hilighted = None
    icons = {}

    color1 = "white"
    color2 = "black"

    rows = 8
    columns = 8

    color_turn = 'White'

    def __init__(self, parent, controller, square_size=64):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Menu",
                            command=lambda: controller.show_frame(Menu))
        button1.pack()

        # self.parent = parent
        # canvas_width = self.columns * square_size
        # canvas_height = self.rows * square_size
        # print(square_size)
        #
        # Frame(parent)
        #
        # self.canvas = Canvas(parent, width=canvas_width, height=canvas_height, background="grey")
        # self.canvas.pack(side="top", fill="both", anchor="c", expand=True)
        # self.canvas.bind("<Configure>")
        # self.canvas.bind("<Button-1>")
        #
        # self.statusbar = Frame(parent, height=64)
        # self.button_quit = Button(self.statusbar, text="New", fg="black", command=self.reset)
        # self.button_quit.pack(side=LEFT, in_=self.statusbar)
        #
        # self.button_save = Button(self.statusbar, text="Save", fg="black")
        # self.button_save.pack(side=LEFT, in_=self.statusbar)
        #
        # self.label_status = Label(self.statusbar, text="   {}'s turn  ".format(self.color_turn), fg="black")
        # self.label_status.pack(side=LEFT, expand=0, in_=self.statusbar)
        #
        # self.button_quit = Button(self.statusbar, text="Quit", fg="black", command=lambda: controller.show_frame(Menu))
        # self.button_quit.pack(side=RIGHT, in_=self.statusbar)
        # self.statusbar.pack(expand=False, fill="x", side='bottom')

    def reset(self):
        print('reset')
