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
    loadImages() #only to do this once before while loop
    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current gamestate. Includes Board and Piece
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
Draw peices on the board using current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]

            if piece != "--": #not empty space
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()