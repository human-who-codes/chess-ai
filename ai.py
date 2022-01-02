"""

create a chess game that can be played with 1 human and 1 computer
chess game is played in the terminal


"""


import chess as c
import regex as re
import os
import random
import time


def clear():
    #clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')


def make_move(board):
    # use AI to make a move
    # takes in a board and returns a move
    # AI is a simple decided move
    lmoves = board.legal_moves
    moves = []
    tboard = board.copy()
    for move in lmoves:
        moves.append(move)
    move = random.choice(moves)
    return move

board = c.Board()
moves = board.legal_moves
turn = "p"
while(True):
    print(board)
    moves = board.legal_moves
    if turn == "p":
        move = input("Enter your move: ")
        if move == "q":
            break
        if(not re.match(r'[a-h][1-8][a-h][1-8]', move)):
            clear()
            print("\nInvalid move\n")
            continue
        m = c.Move.from_uci(move)
        if m in moves:
            board.push(m)
        else:
            clear()
            print("Illegal move\n")
            continue
        turn = "c"

    if turn == "c":
        time.sleep(3)
        move = make_move(board)
        board.push(move)
        turn = "p"

    if board.is_game_over():
        print("Game Over")
        break

    clear()
