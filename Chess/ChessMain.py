"""
This is out main driver file. This will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from multiprocessing import Process, Queue
from Chess import ChessEngine, ChessAi

p.init()
BOARD_WIDTH = BOARD_HEIGHT = 512 #400 is an option
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 #dimension of chess board is 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15 #for animation
IMAGES = {}

'''
load images only once to reduce used space to reduce lagging as loading image is a complex mechanism
Initializing a global dictionary of Images. This will be called exactly once in the main
'''

def loadImages():
    #IMAGES['wp'] = p.image.load("Images/wp.png")  but will be heavy as we need to do this for each file
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note we can access an image from dictionary by saying 'IMAGES['wp']'


'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()
    p.display.set_caption("Chess")  # Set the screen name
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Times New Roman", 15, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False #flag variable for when we should animate
    loadImages() #only to do this once before while loop
    running = True
    sqSelected = () #no square selected initially, keep track of last click of user in tuple (row, column)
    playerClicks = [] #keep track of player clicks, two tuples [(6, 4), (4,4)]
    gameOver = False
    '''
    TO set player set playerOne or playerTwo to True, for Ai false
    '''
    playerOne = True  # If human is playing white then this will be true. If AI then false
    playerTwo = False # Same as above but for black

    AIThinking = False
    moveFinderProcess = None
    moveUndone = False


    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() #(x, y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE

                    if sqSelected == (row, col) or col >= 8: #user clicking same square twice or user clicked move log
                        sqSelected = () #deselect
                        playerClicks = []

                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for both first and second clicks
                    #was that the users' second clock

                    if len(playerClicks) == 2 and humanTurn: #second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        # print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () #reset the user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]


            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
                if e.key == p.K_r: #reset when r is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

        #AI move finder logic
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print('Thinking')
                returnQueue = Queue() #returnquque used to pass data between queues
                moveFinderProcess = Process(target=ChessAi.findBestMoves, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start() #cals findBestMoves(gs, validMoves)

            if not moveFinderProcess.is_alive():
                print('Done Thinking')
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = ChessAi.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
                # print(move.getChessNotation())
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkmate or gs.stalemate:
            gameOver = True
            text = 'Stalemate' if gs.stalemate else 'Black wins by Checkmate' if gs.whiteToMove else 'White wins by Checkmate'
            drawEndGameText(screen, text)


        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current GameState. Includes Board and Piece
'''
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)  #draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of the square
    drawMoveLog(screen, gs, moveLogFont)


'''
Draw Square for chess board. The top left square on chess board is always light(white).
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("dark grey")]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Highlight the square selected and moves for the piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #square selected is a piece that can be mpved i.e white selects white
            #highlight the selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value 0->transparent 255->opaque
            s.fill(p.Color('light blue'))
                            # if gs.whiteToMove:
                            #     s.fill(p.Color('black'))
                            # else:
                            #     s.fill(p.Color('white'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE,move.endRow * SQ_SIZE))


'''
Draw pieces on the board using current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]

            if piece != "--": #not empty space
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw Move Log
'''
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('Black'), moveLogRect)
    moveLog = gs.moveLog
    padding = 5
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + "  "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1]) + " "
        moveTexts.append(moveString)

    movesPerRow = 2
    textY = padding
    lineSpacing = 0

    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j <len(moveTexts):
                text += moveTexts[i + j]
        textObject = font.render(text, True, p.Color('White'))

        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 15 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw the captured piece onto rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = (move.endRow + 1) if move.pieceCaptured[0] == 'b' else (move.endRow - 1)
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(120)


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitica", 32, True, False)
    textObject = font.render(text, False, p.Color('Gray'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2, BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()