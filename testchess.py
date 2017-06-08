#lol
from __future__ import print_function
from copy import deepcopy
import sys

## Helper functions

# Translate a position in chess notation to x,y-coordinates
# Example: c3 corresponds to (2,5)
def to_coordinate(notation):
    x = ord(notation[0]) - ord('a')
    y = 8 - int(notation[1])
    return (x, y)

# Translate a position in x,y-coordinates to chess notation
# Example: (2,5) corresponds to c3
def to_notation(coordinates):
    (x,y) = coordinates
    letter = chr(ord('a') + x)
    number = 8 - y
    return letter + str(number)

# Translates two x,y-coordinates into a chess move notation
# Example: (1,4) and (2,3) will become b4c5
def to_move(from_coord, to_coord):
    return to_notation(from_coord) + to_notation(to_coord)

## Defining board states

# These Static classes are used as enums for:
# - Material.Rook
# - Material.King
# - Material.Pawn
# - Side.White
# - Side.Black
class Material:
    Rook, King, Pawn = ['r','k','p']
class Side:
    White, Black = range(0,2)

# A chesspiece on the board is specified by the side it belongs to and the type
# of the chesspiece
class Piece:
    def __init__(self, side, material):
        self.side = side
        self.material = material


# A chess configuration is specified by whose turn it is and a 2d array
# with all the pieces on the board
class ChessBoard:

    def __init__(self, turn):
        # This variable is either equal to Side.White or Side.Black
        self.turn = turn
        self.board_matrix = None


    ## Getter and setter methods
    def set_board_matrix(self,board_matrix):
        self.board_matrix = board_matrix

    # Note: assumes the position is valid
    def get_boardpiece(self,position):
        (x,y) = position
        return self.board_matrix[y][x]

    # Note: assumes the position is valid
    def set_boardpiece(self,position,piece):
        (x,y) = position
        self.board_matrix[y][x] = piece

    # Read in the board_matrix using an input string
    def load_from_input(self,input_str):
        self.board_matrix = [[None for _ in range(8)] for _ in range(8)]
        x = 0
        y = 0
        for char in input_str:
            if y == 8:
                if char == 'W':
                    self.turn = Side.White
                elif char == 'B':
                    self.turn = Side.Black
                return
            if char == '\r':
                continue
            if char == '.':
                x += 1
                continue
            if char == '\n':
                x = 0
                y += 1
                continue

            if char.isupper():
                side = Side.White
            else:
                side = Side.Black
            material = char.lower()

            piece = Piece(side, material)
            self.set_boardpiece((x,y),piece)
            x += 1

    # Print the current board state
    def __str__(self):
        return_str = ""

        return_str += "   abcdefgh\n\n"
        y = 8
        for board_row in self.board_matrix:
            return_str += str(y) + "  "
            for piece in board_row:
                if piece == None:
                    return_str += "."
                else:
                    char = piece.material
                    if piece.side == Side.White:
                        char = char.upper()
                    return_str += char
            return_str += '\n'
            y -= 1

        turn_name = ("White" if self.turn == Side.White else "Black")
        return_str += "It is " + turn_name + "'s turn\n"

        return return_str

    # Given a move string in chess notation, return a new ChessBoard object
    # with the new board situation
    # Note: this method assumes the move suggested is a valid, legal move
    def make_move(self, move_str):

        start_pos = to_coordinate(move_str[0:2])
        end_pos = to_coordinate(move_str[2:4])

        if self.turn == Side.White:
            turn = Side.Black
        else:
            turn = Side.White

        # Duplicate the current board_matrix
        new_matrix = [row[:] for row in self.board_matrix]

        # Create a new chessboard object
        new_board = ChessBoard(turn)
        new_board.set_board_matrix(new_matrix)

        # Carry out the move in the new chessboard object
        piece = new_board.get_boardpiece(start_pos)
        new_board.set_boardpiece(end_pos, piece)
        new_board.set_boardpiece(start_pos, None)

        return new_board

    def is_king_dead(self, side):
        seen_king = False
        for x in range(8):
            for y in range(8):
                piece = self.get_boardpiece((x,y))
                if piece != None and piece.side == side and \
                        piece.material == Material.King:
                    seen_king = True
        return not seen_king



    # This function should return, given the current board configuation and
    # which players turn it is, all the moves possible for that playerssssssssss
    # It should return these moves as a list of move strings, e.g.
    # [c2c3, d4e5, f4f8]
    # TODO: write an implementation for this function
    def legal_moves(self):
        # we moeten toevoegen dat hij kijkt wiens zet het is
        possible_actions = []
        for x in range(8):
            for y in range(8):
                piece = self.get_boardpiece((x,y))
                if piece != None and piece.side==self.turn and piece.material == Material.King:
                        self.koning_Check(x,y,possible_actions)
                if piece != None and piece.side==self.turn and  piece.material == Material.Rook:
                        self.toren_Check(x,y,possible_actions)
                if piece != None and piece.side==self.turn and   piece.material == Material.Pawn:
                        self.pion_Check(x,y,possible_actions)
        return possible_actions


    pass

    def koning_Check(self,x,y,possible_actions):
        start = (x,y)
        start = to_notation(start)
        pieceself = self.get_boardpiece((x,y))
        for t in range(-1,2):
            for z in range(-1,2):
                move = (x+z, y+t)
                if x+z != -1 and y+t !=-1 and x+z !=8 and y+t !=8 and move !=(x,y):
                    piece = self.get_boardpiece((x+z, y+t))
                    if piece != None and piece.side == pieceself.side:
                        pass
                    else:
                        move = to_notation(move)
                        possible_actions.append(start + move)
        return possible_actions


    def toren_Check(self,x,y,possible_actions):
        start = (x,y)
        pieceself = self.get_boardpiece((x,y))
        #Horizontal Moves
        for t in range(8-x):
            end = (x+t, y)
            if start != end:
                piece = self.get_boardpiece((x+t, y))
                if piece != None :
                    if piece.side == pieceself.side:
                        break
                    if piece.side != pieceself.side:
                        possible_actions.append(to_move(start,end))
                        break
                else:
                    possible_actions.append(to_move(start,end))

        for t in range(x+1):
                if t < 8 :
                    end = (x-t, y)
                    if start != end:
                        piece = self.get_boardpiece((x-t, y))
                        if piece != None:
                            if piece.side == pieceself.side:
                                break
                            if piece.side != pieceself.side:
                                possible_actions.append(to_move(start,end))
                                break
                        else:
                            possible_actions.append(to_move(start,end))

        #Vertical Moves
        for t in range(8-y):
            end = (x, y+t)
            if start != end:
                piece = self.get_boardpiece((x, y+t))
                if piece != None :
                    if piece.side == pieceself.side:
                        break
                    if piece.side != pieceself.side:
                        possible_actions.append(to_move(start,end))
                        break
                else:
                    possible_actions.append(to_move(start,end))

        for t in range(y+1):
                if t < 8 and t > 0:
                    end = (x, y-t)
                    piece = self.get_boardpiece((x, y-t))
                    if start != end:
                        if piece != None :
                            if piece.side == pieceself.side:
                                break
                            if piece.side != pieceself.side:
                                possible_actions.append(to_move(start,end))
                                break
                        else:
                            possible_actions.append(to_move(start,end))

        return possible_actions

    def pion_Check(self,x,y,possible_actions):
        start = (x,y)
        start = to_notation(start)
        pieceself = self.get_boardpiece((x,y))
        if pieceself.side == Side.White:
            move = (x, y-1)
            move = to_notation(move)
            if y !=-1:
                pieces = self.get_boardpiece((x,y-1))
                if pieces == None :
                    possible_actions.append(start + move)
            move = (x+1, y-1)
            move = to_notation(move)
            if y !=-1 and x != 8:
                pieces = self.get_boardpiece((x+1,y-1))
                if pieces != None :
                    if pieces.side != pieceself.side:
                        possible_actions.append(start + move)
            move = (x-1, y-1)
            move = to_notation(move)
            if y !=-1 and x != -1:
                pieces = self.get_boardpiece((x-1,y-1))
                if pieces != None :
                    if pieces.side != pieceself.side:
                        possible_actions.append(start + move)

        if pieceself.side == Side.Black:
            move = (x, y+1)
            move = to_notation(move)
            if y !=-1:
                pieces = self.get_boardpiece((x,y+1))
                if pieces == None :
                    possible_actions.append(start + move)

            move = (x+1, y+1)
            move = to_notation(move)
            if y !=8 and x != 8:
                pieces = self.get_boardpiece((x+1,y+1))
                if pieces != None :
                    if pieces.side != pieceself.side:
                        possible_actions.append(start + move)
            move = (x-1, y+1)
            move = to_notation(move)
            if y !=8 and x != -1:
                pieces = self.get_boardpiece((x-1,y+1))
                if pieces != None :
                    if pieces.side != pieceself.side:
                        possible_actions.append(start + move)
        return possible_actions

    # This function should return, given the move specified (in the format
    # 'd2d3') whether this move is legal
    # TODO: write an implementation for this function, implement it in terms
    # of legal_moves()
    def is_legal_move(self, move):
        moves = self.legal_moves()
        if move in moves:
            return True
        else: return False

# This static class is responsible for providing functions that can calculate
# the optimal move using minimax
class ChessComputer:

    # This method uses either alphabeta or minimax to calculate the best move
    # possible. The input needed is a chessboard configuration and the max
    # depth of the search algorithm. It returns a tuple of (score, chessboard)
    # with score the maximum score attainable and chessboardmove that is needed
    #to achieve this score.
    @staticmethod
    def computer_move(chessboard, depth, alphabeta=False):
        if alphabeta:
            inf = 99999999
            min_inf = -inf
            return ChessComputer.alphabeta(chessboard, depth, min_inf, inf)
        else:
            return ChessComputer.minimax(chessboard, depth)


    # This function uses minimax to calculate the next move. Given the current
    # chessboard and max depth, this function should return a tuple of the
    # the score and the move that should be executed
    # NOTE: use ChessComputer.evaluate_board() to calculate the score
    # of a specific board configuration after the max depth is reached
    # TODO: write an implementation for this function
    @staticmethod
    def minimax(chessboard, depth):
        moves = chessboard.legal_moves()
        if depth == 0 or chessboard.is_king_dead(Side.White) or chessboard.is_king_dead(Side.Black):
            bestValue = ChessComputer.evaluate_board(chessboard, depth)
            return (bestValue, None)
        else:   
            print(chessboard.turn)
             
            while depth > 0:
                if chessboard.turn == 0:
                    bestmove = None
                    bestValue = -float("inf")
                    move = None
                    i = 0
                    #doet het net zovaak als er mogelijke moves zijn
                    while i < len(moves):
                        print(bestmove) 
                        print(bestValue) 
                        new_state = chessboard.make_move(str(moves[i]))
                        print(new_state)
                        
                        score,move = ChessComputer.minimax(new_state, depth-1)
                        move=moves[i]
                        i = i + 1
                        if score > bestValue: # white maximizes her score
                            bestValue = score
                            bestmove = move
                    print(bestmove)            
                    return (bestValue, bestmove)

                else:
                    bestValue = float("inf")
                    bestmove = None
                    i = 0
                    while i < len(moves):
                        new_state = chessboard.make_move(str(moves[i]))
                        print(new_state)
                        score,move = ChessComputer.minimax(new_state, depth-1)
                        i = i + 1
                        if score > bestValue: # white maximizes her score
                            bestValue = score
                            bestmove = move
                    print(bestmove)            
                    return (bestValue, bestmove)
#    def maxValue(chessboard):
#        bestValue = inf
#        return bestValue

#    def minValue(chessboard):
#        bestValue = -inf
#        return bestValue

    # This function uses alphabeta to calculate the next move. Given the
    # chessboard and max depth, this function should return a tuple of the
    # the score and the move that should be executed.
    # It has alpha and beta as extra pruning parameters
    # NOTE: use ChessComputer.evaluate_board() to calculate the score
    # of a specific board configuration after the max depth is reached
    @staticmethod
    def alphabeta(chessboard, depth, alpha, beta):
        return (0, "no implementation written")

    # Calculates the score of a given board configuration based on the
    # material left on the board. Returns a score number, in which positive
    # means white is better off, while negative means black is better of
    @staticmethod
    def evaluate_board(ChessBoard, depth_left):
        boardValue = 0
        for x in range(8):
            for y in range(8):
                piece = ChessBoard.get_boardpiece((x,y))
                if piece != None and piece.side == 0 and piece.material == Material.King:
                    boardValue = boardValue + 100
                if piece != None and piece.side == 1 and piece.material == Material.King:
                    boardValue = boardValue - 100
                if piece != None and piece.side == 0 and piece.material == Material.Rook:
                    possible_actions = []
                    movesrook = len(ChessBoard.toren_Check(x,y,possible_actions))
                    boardValue = boardValue + (5 +movesrook/14)
                if piece != None and piece.side == 1 and piece.material == Material.Rook:
                    possible_actions = []
                    movesrook = len(ChessBoard.toren_Check(x,y,possible_actions))
                    boardValue = boardValue - 5 -movesrook/14
                if piece != None and piece.side == 0 and piece.material == Material.Pawn:
                    possible_actions = []
                    movespawn = len(ChessBoard.pion_Check(x,y,possible_actions))
                    print (ChessBoard.pion_Check(x,y,possible_actions))
                    boardValue = boardValue + (0.5+ movespawn/2)
                if piece != None and piece.side == 1 and piece.material == Material.Pawn:
                    possible_actions = []
                    movespawn = len(ChessBoard.pion_Check(x,y,possible_actions))
                    boardValue = boardValue - 0.5- movespawn/2
        return boardValue

# This class is responsible for starting the chess game, playing and user
# feedback
class ChessGame:
    def __init__(self, turn):

        # NOTE: you can make this depth higher once you have implemented
        # alpha-beta, which is more efficient
        self.depth = 4
        self.chessboard = ChessBoard(turn)

        # If a file was specified as commandline argument, use that filename
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        else:
            filename = "board.chb"

        print("Reading from " + filename + "...")
        self.load_from_file(filename)

    def load_from_file(self, filename):
        with open(filename) as f:
            content = f.read()

        self.chessboard.load_from_input(content)

    def main(self):
        while True:
            print(self.chessboard)

            # Print the current score
            score = ChessComputer.evaluate_board(self.chessboard,self.depth)
            print("Current score: " + str(score))

            # Calculate the best possible move
            new_score, best_move = self.make_computer_move()

            print("Best move: " + str(best_move))
            print("Score to achieve: " + str(new_score))
            print("")
            self.make_human_move()


    def make_computer_move(self):
        print("Calculating best move...")
        return ChessComputer.computer_move(self.chessboard,
                self.depth, alphabeta=False)


    def make_human_move(self):
        # Endlessly request input until the right input is specified
        while True:
            if sys.version_info[:2] <= (2, 7):
                move = raw_input("Indicate your move (or q to stop): ")
            else:
                move = input("Indicate your move (or q to stop): ")
            if move == "q":
                print("Exiting program...")
                sys.exit(0)
            elif self.chessboard.is_legal_move(move):
                break
            print("Incorrect move!")

        self.chessboard = self.chessboard.make_move(move)

        # Exit the game if one of the kings is dead
        if self.chessboard.is_king_dead(Side.Black):
            print(self.chessboard)
            print("White wins!")
            sys.exit(0)
        elif self.chessboard.is_king_dead(Side.White):
            print(self.chessboard)
            print("Black wins!")
            sys.exit(0)

chess_game = ChessGame(Side.White)
chess_game.main()
