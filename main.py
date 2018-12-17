import core.board as board
import core.gui as gui

if __name__ == "__main__":
    board = board.Board()
    GUI = gui.GUI(board)
    GUI.mainloop()
