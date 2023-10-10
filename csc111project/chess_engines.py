"""CSC111 Winter 2023 Project Phase 2: Creating a Simple Chess AI

Module Description
===============================

This module contains the abstract class ChessEngine and other subclasses.
They are all able to make a move given a board in chess.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Erika Liang and Addison Luo.
"""

import chess
import random
import chess_tree
import math
from typing import Optional


class ChessEngine:
    """An abstract class representing an engine that make moves in chess"""
    def make_move(self, board: chess.Board):
        """Return a move to make given the current position on the chess board.

        This class can be subclassed to implement different strategies to make a move.
        """
        raise NotImplementedError


class RandomChessEngine(ChessEngine):
    """A chess engine that makes a valid random move given a board in chess."""
    def make_move(self, board: chess.Board) -> chess.Move:
        """Return a move given the current board. Randomly choose among all valid moves for the given board.

        If there are no valid moves, return chess.Move.null(), which is a null move that does not
        affect the board state.
        """
        legal_moves = list(board.generate_legal_moves())
        if legal_moves:
            return random.choice(legal_moves)
        else:  # there are no legal moves, so return a null move
            return chess.Move.null()


class UserInput(ChessEngine):
    """A chess engine that makes moves based on user input.

    If the user does not input a legal move, they are prompted for a valid move again.

    The user may resign by inputting 'resign'.

    Instance Attributes:
    - resign: a bool representing if the player has resigned or not.
    """
    resign: bool

    def __init__(self):
        """Initialize the user player"""
        self.resign = False

    def make_move(self, board: chess.Board) -> chess.Move:
        """Return a move given the current board. The user inputs a move in SAN format (e.g. e4).

        The .parse_san() function from the chess library checks if the move is valid or invalid due to
        syntax, ambiguity, or being illegal.

        If the move is not a legal move, the user is prompted again until they input a legal move.
        """
        move_is_illegal = True
        move_input = input('What is your next move? ')
        move = chess.Move.null()

        while move_is_illegal:
            try:
                move = board.parse_san(move_input)

                # if the code reachs here, move is a legal move.
                move_is_illegal = False

            except chess.InvalidMoveError:
                if move_input.lower() == 'resign':
                    self.resign = True
                    return move
                move_input = input('Invalid move due to syntax. Please enter a valid move: ')
            except chess.AmbiguousMoveError:
                move_input = input('Invalid move due to ambiguity. Please enter a valid move: ')
            except chess.IllegalMoveError:
                move_input = input('Illegal move. Please enter a valid move: ')

        return move


class TreeChessEngine(ChessEngine):
    """A chess engine that makes moves based on choosing the move that leads to the highest/lowest
    evaluation score in a chess tree.

    Instance Attributes:
    - depth: a integer representing the depth of a chess tree to create after fully
    traversing through the path of the original chess tree.
    """
    depth: int
    _chess_tree: Optional[chess_tree.ChessTree]

    def __init__(self, tree: chess_tree.ChessTree, depth: int):
        """Initialize this chess engine."""
        self._chess_tree = tree
        self.depth = depth

    def make_move(self, board: chess.Board):
        """Return a move given the current board. Choose the move that will lead to the best position
        based on maximizing or minimizing the eval_position"""
        if board.move_stack and self._chess_tree is not None:
            # if there exists at least one move in the move stack and the chess tree exists,
            self._chess_tree = self._chess_tree.find_subtree_by_board(board)

        if self._chess_tree is None or self._chess_tree.get_subtrees() == []:
            # if the chess tree doesn't exist or there are no more subtrees, create and set the new chess tree as
            # one from that position
            self._chess_tree = chess_tree.generate_pruned_chess_tree(board, self.depth, -math.inf, math.inf)

        subtrees = self._chess_tree.get_subtrees()

        if subtrees:
            if board.turn:  # if the player is white, they are trying to maximize the eval_score
                maximized_eval_position_st = max(subtrees, key=lambda subtree: subtree.eval_position)
                self._chess_tree = maximized_eval_position_st
                return maximized_eval_position_st.board.peek()

            else:  # the player is black, they are trying to minimize the eval_score
                minimized_eval_position_st = min(subtrees, key=lambda subtree: subtree.eval_position)
                self._chess_tree = minimized_eval_position_st
                return minimized_eval_position_st.board.peek()
        else:  # code only goes here in the case that generate_pruned_chess_tree returns a tree that has no subtrees,
            #  i.e. one where there are no more legal moves so return a null move
            return chess.Move.null()


class GreedyChessEngine(ChessEngine):
    """A chess engine that chooses moves based on searching for the move that leads to the min/max
    evaluation of position.

    Instance Attributes:
    - depth: an integer representing how deep to search.
    """
    depth: int

    def __init__(self, depth: int):
        """Intialize this chess engine."""
        self.depth = depth

    def make_move(self, board: chess.Board) -> chess.Move:
        """Return a move based on the find_move_by_search algorithm."""
        move = chess_tree.find_move_by_search(board, self.depth)
        return move
