"""

create a chess game that can be played with 1 human and 1 computer
chess game is played in the terminal


"""


import chess as c
import regex as re
import os
import random
import time

piece_values = {'P':-1, 'N':-3, 'B':-3, 'R':-5, 'Q':-9, 'K':0, 'p':1, 'n':3, 'b':3, 'r':5, 'q':9, 'k':0}


def clear():
    #clear the terminal
    #os.system('cls' if os.name == 'nt' else 'clear')
    pass


def make_move(board):
    # use AI to make a move
    # takes in a board and returns a move
    # AI is a simple decided move
    lmoves = board.legal_moves
    moves = {} # dictionary of moves and their scores
    for move in lmoves:
        nboard = board.copy()
        nboard.push(move)
        moves[move] = evaluate_board(nboard)
    best_moves = [move for move in moves if moves[move] == max(moves.values())]
    return random.choice(best_moves)

def evaluate_board(board):
    # evaluate the board from the perspective of the AI
    # return a score from -1 to 1 where 1 is the best for the AI/black
    # and -1 is the best for the human/white
    # return 0 if the board is a draw

    board_score = 0

    # check if the board is over
    if board.is_game_over():
        if board.is_checkmate():
            # checkmate
            if board.turn:
                # black is checkmated
                board_score = -1
            else:
                # white is checkmated
                board_score = 1
        else:
            # draw
            board_score = 0
        return board_score
    
    # check if we have more piece values
    piece_score = 0
    for piece in board.piece_map():
        piece_score += piece_values[board.piece_map()[piece].symbol()]
    return piece_score

    
board = c.Board()
moves = board.legal_moves
turn = "p"
print("Moves are in format 'a1-a2' or startsquare-endsquare\nPress 'q' to quit")
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
        time.sleep(1)
        move = make_move(board)
        print("Computer move: ", move)
        board.push(move)
        turn = "p"

    if board.is_game_over():
        print("Game Over")
        break

    clear()
