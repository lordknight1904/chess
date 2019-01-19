# import Piece
import sys

ABBREVIATIONS = {
 'R': 'Rook',
 'N': 'Knight',
 'B': 'Bishop',
 'Q': 'Queen',
 'K': 'King',
 'P': 'Pawn'
}


# Takes a piece name or abbreviation and returns the corresponding piece instance
def piece(piece, board, color='white'):
    if piece in (None, ' '):
        return
    if len(piece) == 1:
        # We have an abbreviation
        if piece.isupper():
            color = 'white'
        else:
            color = 'black'
        piece = ABBREVIATIONS[piece.upper()]
    module = sys.modules[__name__]
    return module.__dict__[piece](color, board)


class Piece(object):
    __slots__ = ('abbreviation', 'color', 'board')

    def __init__(self, color, board):
        self.color = color
        self.board = board
        if color == 'white':
            self.abbreviation = self.abbreviation.upper()
        elif color == 'black':
            self.abbreviation = self.abbreviation.lower()

    @property
    def name(self): return self.__class__.__name__

    def possible_moves(self, position, orthogonal, diagonal, distance):
        board = self.board
        legal_moves = []
        orth = ((-1, 0), (0, -1), (0, 1), (1, 0))
        diag = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        piece = self

        from_ = board.number_notation(position)
        if orthogonal and diagonal:
            directions = diag+orth
        elif diagonal:
            directions = diag
        elif orthogonal:
            directions = orth

        for x, y in directions:
            collision = False
            for step in range(1, distance+1):
                if collision:
                    break

                if 0 <= from_[0] + step*x < 8 and 0 <= from_[1] + step*y < 8:
                    dest = from_[0]+step*x, from_[1]+step*y
                    if self.board.letter_notation(dest) not in board.occupied('white') + board.occupied('black'):
                        legal_moves.append(dest)
                    elif self.board.letter_notation(dest) in board.occupied(piece.color):
                        collision = True
                    else:
                        legal_moves.append(dest)
                        collision = True

        # legal_moves = filter(board.is_in_bounds, legal_moves)
        return map(board.letter_notation, legal_moves)


class Pawn(Piece):
    abbreviation = 'p'
    def possible_moves(self, position):
        board = self.board
        if self.color == 'white':
            homerow, direction, enemy = 6, -1, 'black'
        else:
            homerow, direction, enemy = 1, 1, 'white'

        legal_moves = []

        # Moving

        blocked = board.occupied('white') + board.occupied('black')
        from_ = board.number_notation(position)
        forward = from_[0], from_[1] + direction
        # print("{}->{}, {}->{}".format(position, board.letter_notation(forward), from_, forward))
        # Can we move forward?
        if board.letter_notation(forward) not in blocked:
            legal_moves.append(forward)
            if from_[1] == homerow:
                # If pawn in starting position we can do a double move
                double_forward = (forward[0], forward[1] + direction)
                if board.letter_notation(double_forward) not in blocked:
                    legal_moves.append(double_forward)

        # Attacking
        for a in range(-1, 1):
            attack = from_[0] + a, from_[1] + direction
            if board.letter_notation(attack) in board.occupied(enemy):
                legal_moves.append(attack)

        # TODO: En passant
        # legal_moves = filter(board.is_in_bounds, legal_moves)
        return map(board.letter_notation, legal_moves)


class Rook(Piece):
    abbreviation = 'r'
    def possible_moves(self, position):
        return super(Rook, self).possible_moves(position, True, False, 8)


class Knight(Piece):
    abbreviation = 'n'
    def possible_moves(self, position):
        board = self.board
        legal_moves = []
        from_ = board.number_notation(position)
        piece = board.get(position)
        deltas = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

        for x,y in deltas:
            if 0 <= from_[0]+x < 8 and 0 <= from_[1]+y < 8:
                dest = from_[0]+x, from_[1]+y
                if(board.letter_notation(dest) not in board.occupied(piece.color)):
                    legal_moves.append(dest)

        # legal_moves = filter(board.is_in_bounds, legal_moves)
        return map(board.letter_notation, legal_moves)


class Bishop(Piece):
    abbreviation = 'b'
    def possible_moves(self, position):
        return super(Bishop,self).possible_moves(position, False, True, 8)


class King(Piece):
    abbreviation = 'k'
    def possible_moves(self, position):
        return super(King, self).possible_moves(position, True, True, 1)


class Queen(Piece):
    abbreviation = 'q'
    def possible_moves(self, position):
        return super(Queen, self).possible_moves(position, True, True, 8)
