"""CSC111 Winter 2023 Project Phase 2: Creating a Simple Chess AI

Module Description
===============================

This module contains the runner functions for the main.
run_game() contains the main loop for the chess game and pushes
moves onto the board by using engines from chess_engines.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Erika Liang and Addison Luo.
"""

import chess
import chess_engines
import chess_tree
import display_helpers
import pygame


def run_game(white_player: chess_engines.ChessEngine,
             black_player: chess_engines.ChessEngine,
             display_game: bool = True) -> chess.Board:
    """Run a chess game between two engines or user input.

    Return the board after the game has finished.
    """
    board = chess.Board()
    screen = None

    if display_game:
        screen = display_helpers.initialize_pygame_window()
        display_helpers.display_board(screen, board)

    while board.outcome() is None:
        white_move = white_player.make_move(board)
        # resign check for white
        if isinstance(white_player, chess_engines.UserInput):
            if white_player.resign:
                break
        board.push(white_move)
        if display_game:
            display_helpers.display_board(screen, board)

        if board.outcome() is not None:  # if white checkmates
            break

        black_move = black_player.make_move(board)
        # resign check for black
        if isinstance(black_player, chess_engines.UserInput):
            if black_player.resign:
                break

        board.push(black_move)
        if display_game:
            display_helpers.display_board(screen, board)

    if display_game:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

    return board


def run_games(num_games: int,
              white_player: chess_engines.ChessEngine,
              black_player: chess_engines.ChessEngine,
              display_game: bool = False,
              print_game: bool = True) -> dict[str, list[int, int]]:
    """Run num_games number of games between two engines.

    Return a dictionary which counts all game outcomes, the values of the dictionary are the number of times
    white/black had that outcome.

    Preconditions:
    - not isinstance(white_player, UserInput)
    - not isinstance(black_player, UserInput)
    """
    stats = {'CHECKMATE': [0, 0], 'STALEMATE': [0, 0], 'INSUFFICIENT_MATERIAL': [0, 0],
             'SEVENTYFIVE_MOVES': [0, 0], 'FIVEFOLD_REPETITION': [0, 0]}
    for i in range(num_games):
        board = run_game(white_player, black_player, display_game)
        termination = str(board.outcome().termination)
        if board.outcome().winner:
            winner = 'White'
        elif board.outcome().winner is not None:
            winner = 'Black'
        else:
            winner = 'None'
        for stat in stats:
            if stat in termination:
                if board.outcome().winner:  # winner was white
                    stats[stat][0] += 1
                elif board.outcome().winner is not None:  # winner was black
                    stats[stat][1] += 1
                else:  # draw
                    stats[stat][0] += 1
                    stats[stat][1] += 1
        if print_game:
            print(f'Game {i} winner: {winner}.')
    for stat in stats:
        if stat == 'CHECKMATE':
            print(f'White: {stat} {stats[stat][0]}/{num_games} ({100.0 * stats[stat][0] / num_games:.2f}%)')
            print(f'Black: {stat} {stats[stat][1]}/{num_games} ({100.0 * stats[stat][1] / num_games:.2f}%)')
        else:
            print(f'Draw: {stat} {stats[stat][0]}/{num_games} ({100.0 * stats[stat][0] / num_games:.2f}%)')
    return stats


def run_example() -> None:
    """Run a single game using the RandomChessEngine against each other.
    """
    display_helpers.initialize_images()
    white_player = chess_engines.RandomChessEngine()
    black_player = chess_engines.RandomChessEngine()
    board = run_game(white_player, black_player)
    print(board.outcome())


# if __name__ == '__main__':
#     run_example()
