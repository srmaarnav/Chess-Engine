"""
This class is responsible for storing all the information about current state of the chess game. It will also be
reponsible for determining the valid moves at the current state. It will also keep a move log
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
