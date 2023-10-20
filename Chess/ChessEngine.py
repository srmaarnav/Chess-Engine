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
        # board for game
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
        # board for testing
        # self.board = [
        #     ["bR", "bN", "--", "--", "bK", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wR", "wN", "--", "--", "wK", "--", "--", "--"]
        # ]

        self.moveFunctions = {'p' : self.getPawnMoves,
                              'R' : self.getRookMoves,
                              'N' : self.getKnightMoves,
                              'B' : self.getBishopMoves,
                              'Q' : self.getQueenMoves,
                              'K' : self.getKingMoves
                              }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = () #coordinates for the square where en passant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    '''
    Takes a move as parameter and executes it. does not work with castling, pawn promotion and en passant
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move to undo later
        self.whiteToMove = not self.whiteToMove #swap player
        #update the king location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #en passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn

        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advance
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()


        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] #moves the rook
                self.board[move.endRow][move.endCol + 1] = "--" #erases the old rook
            else: #queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] #moves the rook
                self.board[move.endRow][move.endCol - 2] = "--" #erases the old rook

        #update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

        #enPassant move log update
        self.enpassantPossibleLog.append(self.enpassantPossible)




    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure there is move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch back the turns
            # update king's position
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave the landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            #undo enpassant right
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            #undo castling rights
            self.castleRightsLog.pop() #get rid of new castle right from the move we are undoing
            self.currentCastlingRight = self.castleRightsLog[-1] #set the current castle rights to the last in the list

            #undo castle moves
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else: #queenside
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

            #for AI
            self.checkmate = False;
            self.stalemate = False;


    '''
    Update the castle rights given a move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.bks = False

        #if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False



    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) #copies current castling rights
        # 1. Generate all possible move
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        # 2. for each moves make the move
        for i in range(len(moves)-1, -1, -1): #when removing from a list go backwards through that list
            self.makeMove(moves[i])
        # 3. generate all opponents move
        # 4. for each of opponents move see if they attack your king
        # 3 and 4 are done by inCheck function
            #first we have generated all white move and make a move
            #then if we call incheck, it checks that for black
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
        # 5. if they attack your king, not a valid move
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves  #for now, we do not worry about checks


    '''
    Determine if the current player is in check
    '''
    # def inCheck(self):
    #     if self.whiteToMove:
    #         return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
    #     else:
    #         return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def inCheck(self):
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
        else:
            kingRow, kingCol = self.blackKingLocation

        # Check for enemy pieces that threaten the king
        enemyColor = 'b' if self.whiteToMove else 'w'

        # Check for knight checks
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knightMoves:
            endRow, endCol = kingRow + m[0], kingCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                piece = self.board[endRow][endCol]
                if piece[0] == enemyColor and piece[1] == 'N':
                    return True  # King is under knight's threat

        # Check for diagonal checks (bishop and queen)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            for i in range(1, 8):
                endRow, endCol = kingRow + d[0] * i, kingCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    piece = self.board[endRow][endCol]
                    if piece[0] == enemyColor:
                        if piece[1] == 'B' or piece[1] == 'Q':
                            return True  # King is under diagonal threat
                        else:
                            break
                    elif piece != '--':
                        break  # Blocked by a friendly piece

        # Check for horizontal and vertical checks (rook and queen)
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for d in directions:
            for i in range(1, 8):
                endRow, endCol = kingRow + d[0] * i, kingCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    piece = self.board[endRow][endCol]
                    if piece[0] == enemyColor:
                        if piece[1] == 'R' or piece[1] == 'Q':
                            return True  # King is under horizontal or vertical threat
                        else:
                            break
                    elif piece != '--':
                        break  # Blocked by a friendly piece

        # Check for pawn checks
        pawnMoves = [(1, -1), (1, 1)] if self.whiteToMove else [(-1, -1), (-1, 1)]
        for m in pawnMoves:
            endRow, endCol = kingRow + m[0], kingCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                piece = self.board[endRow][endCol]
                if piece[0] == enemyColor and piece[1] == 'p':
                    return True  # King is under pawn's threat

        return False  # King is not in check

    '''
    Determine if the enemy can attack square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turn back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # square is under attack
                return True
        return False


    '''
    ALl moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []

        for r in range(len(self.board)): #no. of rows
            for c in range(len(self.board[r])):  #no. of cols in given rows
                turn = self.board[r][c][0]

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves



    '''
    Get all possible moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r - 1][c] == "--": #1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r - 2][c] =="--": #2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0: #capture to left
                if self.board[r - 1][c - 1][0] == "b": #enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= 7: #capture to right
                if self.board[r - 1][c + 1][0] == "b": #enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))


        else: #black pawn moves
            if self.board[r + 1][c] == "--": #1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] =="--": #2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0: #capture to left
                if self.board[r + 1][c - 1][0] == "w": #enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= 7: #capture to right
                if self.board[r + 1][c + 1][0] == "w": #enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))


    '''
        Get all possible moves for the knight located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    '''
        Get all possible moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  #4 diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #bishop can move max of 7
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece break
                        break

                else:  # off board
                    break

    '''
        Get all possible moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down and right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece break
                        break

                else:  # off board
                    break


    '''
        Get all possible moves for the queen located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c , moves)
        self.getRookMoves(r, c, moves)


    '''
        Get all possible moves for the king located at row, col and add these moves to the list
    '''
    # def getKingMoves(self, r, c, moves):
    #     kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    #     allyColor = "w" if self.whiteToMove else "b"
    #     for i in range(8):
    #         endRow = r + kingMoves[i][0]
    #         endCol = c + kingMoves[i][1]
    #         if 0 <= endRow < 8 and 0 <= endCol < 8:
    #             endPiece = self.board[endRow][endCol]
    #             if endPiece[0] != allyColor: #not an ally piece
    #                 moves.append(Move((r, c), (endRow, endCol), self.board))
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for move in kingMoves:
            endRow = r + move[0]
            endCol = c + move[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Generate all valid castle moves for the king at (r, c) and add them to the list
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return #cannot castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.wqs):
            self.getQueensideCastleMoves(r, c, moves)


    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == "--":
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))


    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2): #no need for checking 3rd as king wont pass through it
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs




class Move():
    #maps keys to values
    #key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #pawn promotion
        # self.isPawnPromotion = False
        # if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
        #     self.isPawnPromotion = True
        self.isPawnPromotion = ((self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7))
        #en passant
        # self.isEnpassantMove = False
        # if self.pieceMoved[1] == 'p' and (self.endRow, self.endCol) == enpassantPossible:
        #     self.isEnpassantMove = True
        self.isEnpassantMove = isEnpassantMove
        self.isCapture = self.pieceCaptured != "--"
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        #castle move
        self.isCastleMove = isCastleMove


        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # print(self.moveId)



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

    # overwriting string function
    def __str__(self):
        #castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
            # "O-O" #king side castle
            # "O-O-O" #queen side casdtle

        endSquare = self.getRankFile(self.endRow, self.endCol)
        #pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        #pawn promotion
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                # If it's a capture during pawn promotion, add 'x' and the promotion piece symbol
                return self.colsToFiles[
                    self.startCol] + "x" + endSquare + "Q"  # 'Q' is promotion piece
            else:
                return endSquare + "Q"  # 'Q' is promotion piece

        #other piece moved
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare