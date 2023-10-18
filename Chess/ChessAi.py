import random

pieceScore = {"K" : 0,
              "Q" : 10,
              "R" : 5,
              "B" : 3,
              "N" : 3,
              "p" : 1}
CHECKMATE = 1000
STALEMATE = 0
'''
Picks and returns a random move
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, (len(validMoves)-1))]

'''
Find the best move based on material alone
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        random.shuffle(validMoves)
        opponentMaxScore = -CHECKMATE
        for opponentsMoves in opponentsMoves:
            gs.makeMove(opponentsMoves)
            if gs.checkmate:
                score = -turnMultiplier * CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if (score > opponentMaxScore):
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove



'''
Score the board based on the material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score