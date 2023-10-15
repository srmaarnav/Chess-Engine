"""
This class is responsible for storing all the information about current state of the chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log
"""


class GameState():
    def __init__(self):
        # board is in 8x8 2d list. Each element of the list has two character.
        # first char represents color of piece 'b' or 'w'
        # second character represents type of piece 'n' for knight
        # "--" represents empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True
        self.moveLog = []


    '''
    Takes a move as parameter and executes it. does not work with castling, pawn promotion and en passant
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move to undo later
        self.whiteToMove = not self.whiteToMove #swap player

    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure there is move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch back the turns


    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()  #for now we donot worry about checks



    '''
    ALl moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = [Move((6,4), (4,4), self.board)]

        for r in range(len(self.board)): #no. of rows
            for c in range(len(self.board[r])):  #no. of cols in given rows
                turn = self.board[r][c][0]

                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)

        return moves



    '''
    Get all possible moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        pass

    '''
    Get all possible moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        pass


    # class Move(): nested class is possible but not recommended

class Move():
    #maps keys to values
    #key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveId)



    '''
    overriding the equals method to work for a test move given directly as a tuple of chess squares
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        #can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

