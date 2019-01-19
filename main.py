import chess.board as board
import chess.gui as gui

if __name__ == "__main__":
    board = board.Board()
    GUI = gui.GUI(board)
    GUI.mainloop()
