# Python Chess Engine
A simple chess engine using python

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [TODO](#todo)
* [Instructions](#instructions)
* [Illustrations](#illustrations)


## General info
A simple Chess Engine created using Python. The basic game design is done via the Pygame library. For the AI moves, I have used NegaMax Algorithm with Alpha-Beta Pruning.

## Technologies
* Python 3.11.1
* pygame 2.3.0


## TODO
- [ ] Cleaning up the code 
- [ ] Using numpy arrays instead of 2D lists.
- [ ] Stalemate on 3 repeated moves or 50 moves without capture/pawn advancement.
- [ ] Menu to select player vs player/computer.
- [ ] Try to increase the AI speed

## Instructions
1. Clone this repository.
2. Select whether you want to play versus the computer, against another player locally, or watch the game of the engine playing against itself by setting appropriate flags in lines 55 and 56 of `ChessMain.py`.
3. Run `ChessMain.py`.
4. Enjoy the game!

#### Sic:
* Press `z` to undo a move.
* Press `r` to reset the game.

## Illustration
A sample of a game with AI playing itself.
![image](https://github.com/srmaarnav/Chess-Engine/assets/76389823/9c787b3d-2703-49b4-afae-50b13b2b82ec)
