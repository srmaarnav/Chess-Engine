"""
This is out main driver file. This will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from Chess import ChessEngine

p.init()
WIDTH = HEIGHT = 512 #400 is an option
DIMENSION = 8 #dimension of chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
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
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImages() #only to do this once before while loop
    running = True
    sqSelected = () #no square selected initially, keep track of last click of user in tuple (row, column)
    playerClicks = [] #keep track of player clicks, two tuples [(6, 4), (4,4)]

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if sqSelected == (row, col): #user clicking same square twice
                    sqSelected = () #deselect
                    playerClicks = []

                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both first and second clicks
                #was that the users' second clock

                if len(playerClicks) == 2: #second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #reset the user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]


            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current GameState. Includes Board and Piece
'''
def drawGameState(screen, gs):
    drawBoard(screen)  #draw squares on the board
    drawPieces(screen, gs.board) #draw pieces on top of the square

'''
Draw Square for chess board. The top left square on chess board is always light(white).
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark grey")]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw pieces on the board using current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]

            if piece != "--": #not empty space
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()