import random

pieceScore = {"K" : 0, "Q" : 9, "R" : 5, "B" : 3, "N" : 3, "p" : 1}

# knight_scores = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
#                  [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1],
#                  [0.1, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.1],
#                  [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
#                  [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
#                  [0.1, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.1],
#                  [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1],
#                  [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]]
#
# bishop_scores = [[0.4, 0.3, 0.2, 0.1, 0.1, 0.2, 0.3, 0.4],
#                  [0.3, 0.4, 0.3, 0.2, 0.2, 0.3, 0.4, 0.1],
#                  [0.2, 0.3, 0.4, 0.3, 0.3, 0.4, 0.3, 0.1],
#                  [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
#                  [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
#                  [0.2, 0.3, 0.4, 0.3, 0.3, 0.4, 0.3, 0.1],
#                  [0.3, 0.4, 0.3, 0.2, 0.2, 0.3, 0.4, 0.1],
#                  [0.4, 0.3, 0.2, 0.1, 0.1, 0.2, 0.3, 0.4]]
#
# queen_scores =  [[0.1, 0.1, 0.1, 0.3, 0.1, 0.1, 0.1, 0.1],
#                  [0.1, 0.2, 0.3, 0.3, 0.3, 0.2, 0.2, 0.1],
#                  [0.1, 0.4, 0.3, 0.3, 0.3, 0.4, 0.2, 0.1],
#                  [0.1, 0.2, 0.3, 0.3, 0.3, 0.2, 0.2, 0.1],
#                  [0.1, 0.2, 0.3, 0.3, 0.3, 0.2, 0.2, 0.1],
#                  [0.1, 0.4, 0.3, 0.3, 0.3, 0.4, 0.2, 0.1],
#                  [0.1, 0.1, 0.2, 0.3, 0.3, 0.1, 0.1, 0.1],
#                  [0.1, 0.1, 0.1, 0.3, 0.1, 0.1, 0.1, 0.1]]
#
# rook_scores = [[0.4, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4],
#                [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
#                [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
#                [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
#                [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
#                [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
#                [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
#                [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4]]
#
# white_pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
#                      [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
#                      [0.5, 0.6, 0.6, 0.7, 0.7, 0.6, 0.6, 0.5],
#                      [0.2, 0.3, 0.3, 0.5, 0.5, 0.3, 0.3, 0.2],
#                      [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
#                      [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
#                      [0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1, 0.1],
#                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
#
# black_pawn_scores = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#                      [0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 0.1, 0.1],
#                      [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
#                      [0.1, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.1],
#                      [0.2, 0.3, 0.3, 0.5, 0.5, 0.3, 0.3, 0.2],
#                      [0.5, 0.6, 0.6, 0.7, 0.7, 0.6, 0.6, 0.5],
#                      [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
#                      [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]]
#
#
# piecePositionScores = {"N" : knight_scores,
#                        "B" : bishop_scores,
#                        "Q" : queen_scores,
#                        "R" : rook_scores
#                        "bp" : black_pawn_scores,
#                        "wp" : white_pawn_scores}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

king_scores = [[0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2],
               [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
               [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
               [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
               [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
               [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
               [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
               [0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2]]

piecePositionScores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1],
                         "wK": king_scores,
                         "bK": king_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2
nextMove = None
'''
Picks and returns a random move
'''
def findRandomMove(validMoves):
    if validMoves:
        return validMoves[random.randint(0, (len(validMoves)-1))]
    else:
        return None

'''
Find the best move based on material alone greedy with 2 step min max. Not called in main algorithm
'''
def findBestMoveMaterial(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore = STALEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else :
            opponentMaxScore = -CHECKMATE
            for opponentsMoves in opponentsMoves:
                gs.makeMove(opponentsMoves)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
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
Using min-max algorithm recursively
'''
'''
Helper to make first recurive call
'''
def findBestMoves(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    counter = 0
    # random.shuffle(validMoves)
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    returnQueue.put(nextMove)

'''
Recursive call
'''
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

''''
Nega Max Algorithm
'''
# def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
#     global negaMax
#     print('aaa')
#     if depth == 0:
#         return turnMultiplier * scoreBoard(gs)
#
#     maxScore = -CHECKMATE
#     for move in validMoves:
#         gs.makeMove(move)
#         nextMoves = gs.getValidMoves()
#         score = - findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
#         # score = max(score, maxScore)
#         if score > maxScore:
#             maxScore = score
#             if depth == DEPTH:
#                 nextMove = move
#         gs.undoMove()
#     return maxScore
#

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    else:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)

            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move  # Assign the best move to nextMove

            gs.undoMove()
        return maxScore


''''
Alpha Beta Pruning
'''
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    #move ordering - implement later

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)

        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move  # Assign the best move to nextMove
                print(move, score)
        gs.undoMove()

        if score > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore



'''
New method for scoring the board by taking the entire gamestate.
A postive score from here is good for white.
A negative score from here is good for black.
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.stalemate:
        return STALEMATE #neither side wins

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piece = gs.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "--":
                    piece_position_score = piecePositionScores[piece][row][col]
                if piece[0] == "w":
                    score += pieceScore[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= pieceScore[piece[1]] + piece_position_score
    return score

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