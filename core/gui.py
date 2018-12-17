import tkinter as tk
from tkinter import StringVar
from PIL import Image, ImageTk

LARGE_FONT = ("Verdana", 12)


class GUI(tk.Tk):

    rows = 8
    columns = 8

    def __init__(self, board):
        tk.Tk.__init__(self)
        self.title("Chess")
        # self.geometry("800x800")

        self.chessboard = board
        self.difficulty = StringVar()
        self.color = StringVar()
        self.square_size = 64
        self.status_bar_height = 30
        self.geometry("{}x{}".format(
            self.columns*self.square_size,  # windows width
            self.rows*self.square_size+self.status_bar_height)  # windows height
        )
        # self.resizable(False, False)
        self.difficulty.set("Easy")  # set the default option
        self.color.set("White")  # set the default option

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=False)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Menu, Game):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def select_difficulty(self, value):
        self.difficulty = value

    def select_color(self, value):
        self.color = value


class X_Ruler(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, height=controller.status_bar_height)

        label2 = tk.Label(self, text="Simple Chess Game")
        label2.pack()

        difficulty_choices = {'Hard', 'Normal', 'Easy'}
        difficulty_menu = tk.OptionMenu(self, controller.difficulty, *difficulty_choices, command=controller.select_difficulty)
        tk.Label(self, text="Difficulty")
        difficulty_menu.pack()

        color_choices = {'White', 'Black'}
        color_menu = tk.OptionMenu(self, controller.color, *color_choices, command=controller.select_color)
        tk.Label(self, text="Difficulty")
        color_menu.pack()

        button1 = tk.Button(self, text="Start", command=lambda: controller.show_frame(Game))
        button1.pack()
        button2 = tk.Button(self, text="Quit App", command=controller.destroy)
        button2.pack()


class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, height=controller.status_bar_height)

        label2 = tk.Label(self, text="Simple Chess Game")
        label2.pack()

        difficulty_choices = {'Hard', 'Normal', 'Easy'}
        difficulty_menu = tk.OptionMenu(self, controller.difficulty, *difficulty_choices, command=controller.select_difficulty)
        tk.Label(self, text="Difficulty")
        difficulty_menu.pack()

        color_choices = {'White', 'Black'}
        color_menu = tk.OptionMenu(self, controller.color, *color_choices, command=controller.select_color)
        tk.Label(self, text="Difficulty")
        color_menu.pack()

        button1 = tk.Button(self, text="Start", command=lambda: controller.show_frame(Game))
        button1.pack()
        button2 = tk.Button(self, text="Quit App", command=controller.destroy)
        button2.pack()


class Game(tk.Frame):
    pieces = {}
    selected = None
    selected_piece = None
    highlighted = None
    icons = {}

    color1 = "white"
    color2 = "grey"

    color_turn = 'White'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.parent = parent
        self.canvas_width = self.controller.columns * self.controller.square_size
        self.canvas_height = self.controller.rows * self.controller.square_size

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, background="grey")
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.pack(side="top", fill="both", anchor="c", expand=False)

        self.statusbar = tk.Frame(self, height=self.controller.status_bar_height)
        self.button_quit = tk.Button(self.statusbar, text="New", fg="black", command=self.reset)
        self.button_quit.pack(side=tk.LEFT, in_=self.statusbar)

        self.button_save = tk.Button(self.statusbar, text="Save", fg="black")
        self.button_save.pack(side=tk.LEFT, in_=self.statusbar)

        self.label_status = tk.Label(self.statusbar, text="   {}'s turn  ".format(self.color_turn), fg="black")
        self.label_status.pack(side=tk.LEFT, expand=0, in_=self.statusbar)

        self.button_quit = tk.Button(self.statusbar, text="Quit Match", fg="black", command=lambda: controller.show_frame(Menu))
        self.button_quit.pack(side=tk.RIGHT, in_=self.statusbar)
        self.statusbar.pack(expand=True, fill="x", side='bottom')

        self.refresh()
        self.draw_pieces()

    def draw_pieces(self):
        self.canvas.delete("piece")
        for coord, piece in self.controller.chessboard.items():
            x, y = self.controller.chessboard.number_notation(coord)
            # print("{}: {}, {}".format(coord, x, y))
            if piece is not None:
                filename = "img/{}{}.png".format(piece.color, piece.abbreviation.lower())
                piece_name = "{}{}{}".format(piece.abbreviation, x, y)

                if filename not in self.icons:
                    self.icons[filename] = ImageTk.PhotoImage(file=filename, width=32, height=32)

                self.add_piece(piece_name, self.icons[filename], x, y)

                # self.place_piece(piece_name, x, y)

    def add_piece(self, name, image, row=0, column=0):
        # Add a piece to the playing board
        self.canvas.create_image(0, 0, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, row, column)

    def place_piece(self, name, row, column):
        # Place a piece at the given row/column
        self.pieces[name] = (row, column)
        square_size = self.controller.square_size
        x0 = (row * square_size) + int(square_size/2)
        y0 = (column * square_size) + int(square_size/2)
        self.canvas.coords(name, x0, y0)

    def reset(self):
        print('reset')

    def move(self, p1, p2):
        # print("{} -> {}".format(p1, p2))
        piece = self.controller.chessboard[p1]
        dest_piece = self.controller.chessboard[p2]
        if dest_piece is None or dest_piece.color != piece.color:
            self.controller.chessboard.move(p1,p2)

    def refresh(self, event={}):
        self.canvas.delete("square")
        color = self.color2

        for row in range(self.controller.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.controller.columns):
                x1 = (row * self.controller.square_size)
                y1 = (col * self.controller.square_size)
                x2 = x1 + self.controller.square_size
                y2 = y1 + self.controller.square_size

                if (self.selected is not None) and (row, col) == self.selected:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="orange", tags="square")
                else:
                    if self.highlighted is not None and (row, col) in self.highlighted:
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="spring green", tags="square")
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.place_piece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def callback(self, event):
        col_size = row_size = self.controller.square_size

        current_column = event.x // col_size
        current_row = event.y // row_size

        position = self.controller.chessboard.letter_notation((current_column, current_row))
        piece = self.controller.chessboard[position]
        print("{}:{} {}, {}".format(position, piece.abbreviation if piece is not None else '?', current_column, current_row))

        skip = False
        if self.selected_piece:
            self.move(self.selected_piece[1], position)
            self.selected_piece = None
            self.highlighted = None
            self.pieces = {}
            self.draw_pieces()
            skip = True

        if piece is not None and not skip:
            self.highlight(position, piece)
        self.refresh()

    def highlight(self, pos, piece):
        if piece is not None and (piece.color == self.controller.chessboard.player_turn):
            # print("{}: {}".format(pos, piece.abbreviation))
            self.selected_piece = (self.controller.chessboard[pos], pos)
            self.highlighted = list(map(self.controller.chessboard.number_notation,
                                        (self.controller.chessboard[pos].possible_moves(pos))
                                        )
                                    )
            # self.highlighted = self.controller.chessboard[pos].possible_moves(pos)
            # print(self.highlighted)
