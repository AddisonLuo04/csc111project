"""CSC111 Winter 2023 Project Phase 2: Creating a Simple Chess AI

Module Description
===============================

This module is the main interface for the user. Calls supporting functions
and handles user input.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Erika Liang and Addison Luo.
"""
import math
import sys

import chess
import chess_tree
import chess_engines
import display_helpers
import runner


def main():
    """The function that will handle user input and calling all other functions."""
    display_helpers.initialize_images()
    user_input = input("Welcome to our program! Enter 0 to stop the program. What would you like to do?\n"
                       "1. Watch a game between two RandomChessEngines/TreeChessEngines\n"
                       "2. Play a game against a RandomChessEngine/TreeChessEngine\n"
                       "3. Get statistics about games between Engines\n"
                       "Enter 1, 2, or 3: ")
    while user_input not in '0123':
        user_input = input("Please enter a valid input or enter 0 to stop the program. ")

    if user_input == '0':
        sys.exit()

    elif user_input == '1':
        next_input = input("What game would you like to watch? Enter 0 to stop the program.\n"
                           "1. RandomChessEngine vs. RandomChessEngine\n"
                           "2. RandomChessEngine vs. TreeChessEngine\n"
                           "Enter 1 or 2. ")
        while next_input not in '012':
            next_input = input("Please enter a valid input or enter 0 to stop the program. ")

        if next_input == '0':
            sys.exit()
        elif next_input == '1':
            white_player = chess_engines.RandomChessEngine()
            black_player = chess_engines.RandomChessEngine()
            board = runner.run_game(white_player, black_player)
            print(f'Winner: {board.outcome().winner}, ' + str(board.outcome().termination)[12:])

    elif user_input == '2':
        colour_input = input("What colour would you like to play as?:\n"
                             "1. White\n"
                             "2. Black\n"
                             "Enter 1 or 2. ")
        print("When playing, please enter moves in SAN notation, e.g. Pawn to e4 is: e4, Knight to f3 is: Nf3\n"
              "Type 'resign' to quit while playing.")
        opponent = input("What opponent would you like to play against?:\n"
                         "1. RandomChessEngine\n"
                         "2. TreeChessEngine\n"
                         "Enter 1 or 2. ")

        while colour_input not in '012' or opponent not in '012':
            print('Invalid input. \n')
            colour_input = input("What colour would you like to play as?:\n"
                                 "1. White\n"
                                 "2. Black\n"
                                 "Enter 1 or 2. ")
            opponent = input("What opponent would you like to play against?:\n"
                             "1. RandomChessEngine\n"
                             "2. TreeChessEngine\n"
                             "Enter 1 or 2. ")

        if colour_input == '0' or opponent == '0':
            sys.exit()

        elif colour_input == '1':
            if opponent == '1':
                white_player = chess_engines.UserInput()
                black_player = chess_engines.RandomChessEngine()
            else:
                white_player = chess_engines.UserInput()
                depth = 3
                pruned_tree = chess_tree.generate_pruned_chess_tree(chess.Board(), depth, -math.inf, math.inf)
                black_player = chess_engines.TreeChessEngine(pruned_tree, depth)
            runner.run_game(white_player, black_player)

        elif colour_input == '2':
            if opponent == '1':
                white_player = chess_engines.RandomChessEngine()
                black_player = chess_engines.UserInput()
            else:
                depth = 3
                pruned_tree = chess_tree.generate_pruned_chess_tree(chess.Board(), depth, -math.inf, math.inf)
                white_player = chess_engines.TreeChessEngine(pruned_tree, depth)
                black_player = chess_engines.UserInput()
            runner.run_game(white_player, black_player)

    elif user_input == '3':
        next_input = input("What games would you like to compute statistics for? Enter 0 to stop the program.\n"
                           "1. RandomChessEngine vs. RandomChessEngine\n"
                           "2. RandomChessEngine vs. TreeChessEngine (takes much longer for one game to be completed)\n"
                           "Enter 1 or 2. ")
        while next_input not in '012':
            next_input = input("Please enter a valid input or enter 0 to stop the program. ")

        if next_input == '0':
            sys.exit()
        elif next_input == '1':
            num_games = input('How many games would you like to compute statistics for? ')
            while not num_games.isdigit():
                num_games = input('Please enter a valid number of games you would like to compute statistics for: ')

            num_games = int(num_games)
            white_player = chess_engines.RandomChessEngine()
            black_player = chess_engines.RandomChessEngine()
            runner.run_games(num_games, white_player, black_player)

        elif next_input == '2':
            print("Computing statistics for 1 game. This may take several minutes...")
            num_games = 1
            white_player = chess_engines.RandomChessEngine()
            depth = 3
            pruned_tree = chess_tree.generate_pruned_chess_tree(chess.Board(), depth, -math.inf, math.inf)
            black_player = chess_engines.TreeChessEngine(pruned_tree, depth)
            runner.run_games(num_games, white_player, black_player)


if __name__ == '__main__':
    main()
