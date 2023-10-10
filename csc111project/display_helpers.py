"""CSC111 Winter 2023 Project Phase 2: Creating a Simple Chess AI

Module Description
===============================

This module contains the helper functions for displaying a game of
chess using pygame. Images are from https://en.wikipedia.org/wiki/Chess_piece.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Erika Liang and Addison Luo.
"""

import pygame
import chess
WIDTH = 400
HEIGHT = 400
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
IMAGES = {}
PIECES = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bp', 'bn', 'bb', 'br', 'bq', 'bk']


def initialize_images() -> None:
    """This will initalize the .png images for each piece into a global variable for the display board.
    This will only be called one time in the main.
    """
    # Consistent with the chess library symbols for each piece,
    # capital letters represent white pieces and lowercase, black.
    #
    # w for white, b for black.
    # Each letter is the starting letter of the piece, except N, which is for the knight.
    for piece in PIECES:
        # piece[1] is so that we can set the key in IMAGES as just the second letter which represents the piece in FEN
        IMAGES[piece[1]] = pygame.transform.scale(
            pygame.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def initialize_pygame_window() -> pygame.Surface:
    """Initialize and return a new pygame window with the WIDTH and HEIGHT global variables."""
    pygame.display.init()

    screen_width = WIDTH
    screen_height = HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((255, 255, 255))  # Fill screen with white
    pygame.display.set_caption("Chess Game")
    pygame.display.flip()
    pygame.event.clear()

    return screen


def display_board(screen, board: chess.Board) -> None:
    """Given a specific position on the board of a chess game, displays the board and pieces."""
    # drawing the board
    # notice that a chess board is always configured to where the top left corner square is a light square.
    colours = [(222, 184, 135), (139, 115, 85)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # notice that if we denote each square as a tuple (row, col), if we sum the row and col,
            # light squares will have an even sum while dark squares have an odd sum.
            colour = colours[(row + col) % 2]
            pygame.draw.rect(screen, colour, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                                         SQUARE_SIZE, SQUARE_SIZE))

    # drawing the pieces
    fen = board.board_fen()  # get the FEN string of the board
    # e.g. the starting position FEN is: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

    row_num = 0
    col_num = 0

    for rank in fen.split('/'):  # split the FEN string into 8 strings representing each rank for the position
        for char in rank:
            if char not in '12345678':  # consecutive empty spaces are denoted with numbers in FEN
                screen.blit(IMAGES[char], pygame.Rect(col_num * SQUARE_SIZE, row_num * SQUARE_SIZE,
                                                      SQUARE_SIZE, SQUARE_SIZE))
                col_num = (col_num + 1) % 8
            else:
                # add the number of empty spaces to col_num so the next iteration starts at the correct col
                col_num += int(char)

        # reset column num back to 0 and increment row_num by 1 to start at the left of the next row
        col_num = 0
        row_num += 1

    pygame.display.update()
