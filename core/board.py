import core.pieces as pieces
import re
from copy import deepcopy

# FEN_STARTING = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
# FEN_STARTING = 'RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr w KQkq - 0 1'
# FEN_STARTING = 'RNBQKBNR/8/8/8/8/8/pppppppp/rnbqkbnr w KQkq - 0 1'
FEN_STARTING = 'RNBQKBNR/8/8/8/8/8/8/6k w KQkq - 0 1'
RANK_REGEX = re.compile(r"^[A-Z][1-8]$")


class Board(dict):

    axis_y = tuple(range(1, 9))
    axis_x = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')

    captured_pieces = {'white': [], 'black': []}
    castling = '-'
    player_turn = None
    en_passant = '-'
    halfmove_clock = 0
    fullmove_number = 1
    history = []
    winner = None
    is_end = False

    def __init__(self, fen=None):
        dict.__init__(self)
        if fen is None:
            self.load(FEN_STARTING)
        else:
            self.load(fen)

    def __getitem__(self, coord):
        if isinstance(coord, str):
            coord = coord.upper()
            if not re.match(RANK_REGEX, coord.upper()): raise KeyError
        elif isinstance(coord, tuple):
            coord = self.letter_notation(coord)
        try:
            return super(Board, self).__getitem__(coord)
        except KeyError:
            return None

    def load(self, fen):
        self.clear()
        # Split data
        fen = fen.split(' ')
        # Expand blanks

        fen[0] = re.compile(r'\d').sub(lambda a: ' ' * int(a.group(0)), fen[0])

        for x, row in enumerate(fen[0].split('/')):
            for y, letter in enumerate(row):
                if letter == ' ':
                    continue
                coord = self.letter_notation((y, 7-x))
                self[coord] = pieces.piece(letter, self)

        # for k in self:
        #     print("{} at {}".format(self[k].abbreviation, k))

        if fen[1] == 'w':
            self.player_turn = 'white'
        else:
            self.player_turn = 'black'

        self.castling = fen[2]
        self.en_passant = fen[3]
        self.halfmove_clock = int(fen[4])
        self.fullmove_number = int(fen[5])

    def encode_x(self, index):
        return self.axis_x[index]

    def decode_x(self, letter):
        return self.axis_x.index(letter)

    def encode_y(self, index):
        return self.axis_y[-index-1]

    def decode_y(self, number):
        return abs(int(number)-8)

    # from coord to word
    def letter_notation(self, coord):
        return str(self.encode_x(coord[0])) + str(self.encode_y(coord[1]))

    # from word to array indexes
    def number_notation(self, coord):
        return self.decode_x(coord[0]), self.decode_y(coord[1])

    def occupied(self, color):
        # Return a list of coordinates occupied by `color`
        result = []
        # if(color not in ("black", "white")): raise InvalidColor

        for coord in self:
            if self[coord].color == color:
                result.append(coord)
        return result

    def is_king(self, piece):
        return isinstance(piece, pieces.King)
    
    def get_king_position(self, color):
        for pos in self.keys():
            if self.is_king(self[pos]) and self[pos].color == color:
                return pos

    def get_king(self, color):
        return self[self.get_king_position(color)]

    def is_in_check(self, color):
        king = self.get_king(color)
        enemy = self.get_enemy(color)
        return king in map(self.__getitem__, self.all_possible_moves(enemy))

    def is_in_check_after_move(self, p1, p2):
        # Create a temporary board
        tmp = deepcopy(self)
        tmp._do_move(p1, p2)
        return tmp.is_in_check(self[p1].color)

    '''
        Return a list of `color`'s possible moves.
        Does not check for check.
    '''
    def all_possible_moves(self, color):
        result = []
        for coord in self.keys():
            if (self[coord] is not None) and self[coord].color == color:
                moves = self[coord].possible_moves(coord)
                if moves:
                    result += moves
        return result

    def move(self, p1, p2):
        piece = self[p1]
        dest = self[p2]

        # prevent player taking wrong turn
        if self.player_turn != piece.color:
            return
            # raise NotYourTurn("Not " + piece.color + "'s turn!")

        enemy = self.get_enemy(piece.color)
        possible_moves = piece.possible_moves(p1)
        # 0. Check if p2 is in the possible moves
        if p2 not in possible_moves:
            return
            # raise InvalidMove

        # If enemy has any moves look for check
        if self.all_possible_moves(enemy):
            if self.is_in_check_after_move(p1, p2):
                return
                # raise Check
        elif not possible_moves:
            self.is_end = True
            return
            # raise Draw

        if not possible_moves and self.is_in_check(piece.color):
            self.is_end = True
            self.winner = self.get_enemy(piece.color)
            print("{}, winner is: {}".format(self.is_end, self.winner))
            return
            # raise CheckMate
        else:
            self._do_move(p1, p2)
            self._finish_move(piece, dest, p1, p2)

    '''
        Move a piece without validation
    '''
    def _do_move(self, p1, p2):
        piece = self[p1]
        del self[p1]
        self[p2] = piece

    @staticmethod
    def get_enemy(color):
        return 'black' if color == 'white' else 'white'

    '''
        Set next player turn, count moves, log moves, etc.
    '''
    def _finish_move(self, piece, dest, p1, p2):
        enemy = self.get_enemy(piece.color)
        if piece.color == 'black':
            self.fullmove_number += 1
        self.halfmove_clock += 1
        self.player_turn = enemy
        abbr = piece.abbreviation
        if abbr == 'P':
            # Pawn resets halfmove_clock
            self.halfmove_clock = 0
        if dest is None:
            # No capturing
            movetext = abbr + p2
        else:
            # Capturing
            movetext = abbr + p2
            # Capturing resets halfmove_clock
            self.halfmove_clock = 0

        self.history.append(movetext)
