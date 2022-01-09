"""

create a chess game that can be played with 1 human and 1 computer
chess game is played in the terminal


"""

import pygame
import pygame.mouse
import chess as c
import regex as re
import os
import random
import time
import sys
import math

piece_values = {'P': -1, 'N': -3, 'B': -3, 'R': -5, 'Q': -9,
                'K': 0, 'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}

# add arrays that say where the best placement for pieces are to the board in 8x8 format


# all pawn_squares are 0
pawn_squares = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                [0.5, 0.5, 1, 1, 1, 1, 0.5, 0.5],
                [0.5, 0.5, 1, 1, 1, 1, 0.5, 0.5],
                [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

# best knight squares are in the center of the board
knight_squares = [[-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, 0, 0, 0, 0, 0, 0, -1],
                  [-1, 0, 1, 1, 1, 1, 0, -1],
                  [-1, 0, 1, 2, 2, 1, 0, -1],
                  [-1, 0, 1, 2, 2, 1, 0, -1],
                  [-1, 0, 1, 1, 1, 1, 0, -1],
                  [-1, 0, 0, 0, 0, 0, 0, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1]]

rook_squares = [[-1, -1, -1, -1, -1, -1, -1, -1],
                [-1, 0, 0, 0, 0, 0, 0, -1],
                [-1, 0, 1, 1, 1, 1, 0, -1],
                [-1, 0, 1, 2, 2, 1, 0, -1],
                [-1, 0, 1, 2, 2, 1, 0, -1],
                [-1, 0, 1, 1, 1, 1, 0, -1],
                [-1, 0, 0, 0, 0, 0, 0, -1],
                [-1, -1, -1, 1, 1, -1, -1, -1]]

# bishops are best on the long diagonals of the board
bishop_squares = [[2, -1, -1, -1, -1, -1, -1, 2],
                  [-1, 1, 1, 1, 1, 1, 1, -1],
                  [-1, 1, 2, 2, 2, 2, 1, -1],
                  [-1, 1, 2, 3, 3, 2, 1, -1],
                  [-1, 1, 2, 3, 3, 2, 1, -1],
                  [-1, 1, 2, 2, 2, 2, 1, -1],
                  [-1, 1, 1, 1, 1, 1, 1, -1],
                  [2, -1, -1, -1, -1, -1, -1, 2]]


queen_squares = [[-1, -1, -1, -1, -1, -1, -1, -1],
                 [-1, 0, 0, 0, 0, 0, 0, -1],
                 [-1, 0, 1, 1, 1, 1, 0, -1],
                 [-1, 0, 1, 2, 2, 1, 0, -1],
                 [-1, 0, 1, 2, 2, 1, 0, -1],
                 [-1, 0, 1, 1, 1, 1, 0, -1],
                 [-1, 0, 0, 0, 0, 0, 0, -1],
                 [-1, -1, -1, -1, -1, -1, -1, -1]]

# king_squares want to be in the sides of the board
king_squares = [[2, 2, 1, 0.5, 0.5, 1, 2, 2],
                [2, 1, 0.5, 0, 0, 0.5, 1, 2],
                [1, 0.5, 0, 0, 0, 0, 0.5, 1],
                [0.5, 0, 0, 0, 0, 0, 0, 0.5],
                [0.5, 0, 0, 0, 0, 0, 0, 0.5],
                [1, 0.5, 0, 0, 0, 0, 0.5, 1],
                [2, 1, 0.5, 0, 0, 0.5, 1, 2],
                [2, 2, 0.5, 0.5, 0.5, 0.5, 2, 2]]

def letter_to_piece(letter):
    # convert a letter where P is a white pawn and p is a black pawn
    # to a unicode character for that piece
    color = "black" if letter.upper() != letter else "white"
    piece = None
    if letter.upper() == "P":
        piece = "\u2659" if color == "white" else "\u265F"
    elif letter.upper() == "N":
        piece = "\u2658" if color == "white" else "\u265E"
    elif letter.upper() == "B":
        piece = "\u2657" if color == "white" else "\u265D"
    elif letter.upper() == "R":
        piece = "\u2656" if color == "white" else "\u265C"
    elif letter.upper() == "Q":
        piece = "\u2655" if color == "white" else "\u265B"
    elif letter.upper() == "K":
        piece = "\u2654" if color == "white" else "\u265A"
    else:
        return " "
    return piece


def clear(window):
    # clear pygame window
    window.fill((255, 255, 255))


def setup_pygame():
    # setup pygame window
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Chess')
    return window, clock

def draw_pieces(window):
    # draw pieces with letters on top of squares
    pieces = board.piece_map()
    for thing in pieces.keys():
        piece = pieces[thing]
        if piece.symbol() == piece.symbol().upper():
            color = (255, 255, 255)
            ocolor = (0, 0, 0)
        else:
            color = (0, 0, 0)
            ocolor = (255, 255, 255)
        x, y = get_position(thing)
        # get square_color from x and y coordinates
        if x % 2 == 0:
            if y % 2 == 0:
                square_color = (255, 255, 255)
            else:
                square_color = (0, 0, 0)
        
        x *= 100
        y *= 100

        pygame.draw.circle(window, color, (x + 50, y + 50), 45, 0)
        font = pygame.font.SysFont('segoeuisymbol', 60)
        text = font.render(letter_to_piece(piece.symbol()), False, ocolor)
        window.blit(text, (x + 50 - text.get_width() // 2, y + 50 - text.get_height() // 2))
    


def draw_board(window):
    # draw the board with pygame
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                pygame.draw.rect(window, (255, 255, 255),
                                 (col * 100, row * 100, 100, 100))
            else:
                pygame.draw.rect(window, (0, 0, 0),
                                 (col * 100, row * 100, 100, 100))

    draw_pieces(window)    


    pygame.display.flip()

def get_position(piece):
    # piece is a number from 0 - 63
    # returns a tuple in form (row, col)
    # row is a number from 0 - 7
    # col is a number from 0 - 7

    row = piece // 8
    col = piece % 8
    return (row, col)

def get_notation(pixel):
    # pixel should be a tuple in form (x, y)
    # pixel x and y are from 0 to 800
    # the x is the number and the y is the letter
    # convert pixel to 'e4' notation

    x = pixel[0] // 100 + 1
    y = pixel[1] // 100
    return chr(y + 97) + str(x)

def make_move(board):
    # use AI to make a move
    # takes in a board and returns a move
    # AI is a simple decided move
    score, move = minmax(board, 2, .01, -.01, True)
    print(score, move)
    return move

def minmax(board, depth, alpha, beta, is_max):
    # minmax algorithm
    if depth == 0:
        return evaluate_board(board, c.BLACK), None
    if is_max:
        best_score = 0
        best_move = None
        for move in board.legal_moves:
            nboard = board.copy()
            nboard.push(move)
            score, _ = minmax(nboard, depth - 1, alpha, beta, False)
            if score > best_score or best_move is None:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if beta >= alpha:
                print("max")
                break
        return best_score, best_move
    else:
        best_score = 0
        best_move = None
        for move in board.legal_moves:
            nboard = board.copy()
            nboard.push(move)
            score, _ = minmax(nboard, depth - 1, alpha, beta, True)
            if score < best_score or best_move is None:
                best_score = score
                best_move = move
            beta = min(beta, score)
            if beta >= alpha:
                print("min")
                break
        return best_score, best_move






def evaluate_board(board, team):
    # board is a chess.Board object
    # evaluate the board from the perspective of the AI
    # return a score from -1 to 1 where 1 is the best for the AI/black
    # and -1 is the best for the human/white
    # return 0 if the board is a draw
    board_score = 0
    if team == c.BLACK:
        oteam = c.WHITE
    else:
        oteam = c.BLACK
    # check if the board is over
    if board.is_game_over():
        if board.is_checkmate():
            # if black is checkmated, return -1
            if board.turn == team:
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
        piece_score += piece_values[board.piece_map()[piece].symbol()] * 10
    board_score += piece_score
    # check positioning of pieces and add to score from the squares arrays
    for piece in board.piece_map():
        pos = get_position(piece)
        symbol = board.piece_map()[piece].symbol().upper()
        sm = 0
        if board.piece_map()[piece].color == team:
            sm = 1
        else:
            sm = -1

        if symbol == 'P':
            board_score += pawn_squares[pos[0]][pos[1]] * sm
        elif symbol == 'N':
            board_score += knight_squares[pos[0]][pos[1]] * sm
        elif symbol == 'B':
            board_score += bishop_squares[pos[0]][pos[1]] * sm
        elif symbol == 'R':
            board_score += rook_squares[pos[0]][pos[1]] * sm
        elif symbol == 'Q':
            board_score += queen_squares[pos[0]][pos[1]] * sm
        elif symbol == 'K':
            board_score += king_squares[pos[0]][pos[1]] * sm

    return board_score


window, clock = setup_pygame()

board = c.Board()
moves = board.legal_moves
turn = "p"
from_square = None
to_square = None
print("Moves are in format 'a1a2' or startend\nPress 'q' to quit")





# game loop
while(True):
    clock.tick(60)
    clear(window)
    draw_board(window)

    moves = board.legal_moves
    if turn == "p":
        
        if from_square != None and to_square != None:
            move = get_notation(from_square) + get_notation(to_square)
            print(move)
            # checks if the inputs squares are legal and if so makes the move
            move = c.Move(c.Square(c.parse_square(move[0] + move[1])), c.Square(c.parse_square(move[2] + move[3])))
            if move in moves or c.Move(move.from_square, move.to_square, promotion=c.QUEEN) in moves:
                move = board.find_move(move.from_square, move.to_square)
                board.push(move)
                turn = "c"
                from_square = None
                to_square = None
            else:
                print("Illegal move\n")
                from_square = None
                to_square = None
                continue
            turn = "c"

    elif turn == "c":
        move = make_move(board)
        print("Computer move: ", move)
        board.push(move)
        turn = "p"

    if board.is_game_over():
        print("Game Over")
        break

    # check if the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if from_square == None:
                from_square = pygame.mouse.get_pos()
            elif to_square == None:
                to_square = pygame.mouse.get_pos()
            else:
                pass
pygame.quit()
