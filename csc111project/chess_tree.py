"""CSC111 Winter 2023 Project Phase 2: Creating a Simple Chess AI

Module Description
===============================

This module contains the ChessTree class and other functions that help
in searching and evaluating the board.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Erika Liang and Addison Luo.
"""
from __future__ import annotations

from typing import Optional

import chess
import math

# piece values using Michniewski's piece values. This will be used to calculate the score of the current board
piece_vals = {chess.PAWN: 100,
              chess.KNIGHT: 320,
              chess.BISHOP: 330,
              chess.ROOK: 500,
              chess.QUEEN: 900,
              chess.KING: 200000}

# piece-square values: bonus values depending on which pieces are on which square
pawns_table_w = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

pawns_table_b = list(reversed(pawns_table_w))

knights_table_w = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

knights_table_b = list(reversed(knights_table_w))

bishops_table_w = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

bishops_table_b = list(reversed(bishops_table_w))

rooks_table_w = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

rooks_table_b = list(reversed(rooks_table_w))

queens_table_w = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

queens_table_b = list(reversed(queens_table_w))

kings_table_w = [
    20, 30, 10, 00, 0, 10, 30, 20,
    20, 20, 00, 00, 00, 00, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

kings_table_b = list(reversed(kings_table_w))


class ChessTree:
    """A decision tree for Chess moves. Each node in the tree stores a valid move in Chess.

    Instance Attributes:
    - board: a representation of a current board in chess, from the chess library
    - eval_position: an evaluation of how "good" the board is for each player, determined by the evalulate_position()

    Representation Invariants:
    - self.board is a valid position of chess
    - all(key == self._subtrees[key].board.board_fen() for key in self._subtrees)
    """
    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the chess trees after a possible
    #      move by the current player. This dictionary is a mapping where the board's
    #      FEN string is the key and the associated values are the ChessTrees
    #      See the last representation invariant above.
    board: chess.Board
    eval_position: float
    _subtrees: dict[str, ChessTree]

    def __init__(self, board: chess.Board, eval_position: float) -> None:
        """Initialize a new ChessTree."""
        self.board = board
        self.eval_position = eval_position
        self._subtrees = {}

    def get_subtrees(self) -> list[ChessTree]:
        """Returns a list containing all the subtrees."""
        return list(self._subtrees.values())

    def find_subtree_by_board(self, board: chess.Board) -> Optional[ChessTree]:
        """Return the subtree corresponding to the given board.

        Return None if no subtree corresponds to that board.
        """
        fen = board.board_fen()
        if fen in self._subtrees:
            return self._subtrees[fen]
        else:
            return None

    def add_subtree(self, subtree: ChessTree) -> None:
        """Add a subtree to this chess tree."""
        fen = subtree.board.board_fen()
        board_copy = subtree.board.copy()
        subtree.board = board_copy
        self._subtrees[fen] = subtree

    def __str__(self) -> str:
        """Return a string representation of this tree."""
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.

        Preconditions:
            - depth >= 0
        """
        if self.board.turn:
            turn_desc = "White's move"
        else:
            turn_desc = "Black's move"

        if self.board.move_stack:
            move_desc = f'{self.board.peek()} -> {turn_desc}\n'
        else:
            move_desc = "start\n"
        str_so_far = '  ' * depth + move_desc
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(depth + 1)
        return str_so_far

    def size(self) -> int:
        """Return the size of this subtree."""
        if len(self._subtrees) == 0:
            return 1
        else:
            size_so_far = 0
            for key in self._subtrees:
                subtree = self._subtrees[key]
                size_so_far += subtree.size()
            return size_so_far


################################################################################
# Functions for generating chess trees
################################################################################
def generate_chess_tree(board: chess.Board, d: int) -> ChessTree:
    """Generate a complete chess tree of depth d for all valid moves from the current board.

    For the returned ChessTree:
        - Its board is the given board.
        - It contains all possible move sequences of length <= d from the board.
        - If d == 0, a size-one ChessTree is returned.

    Note, this grows rather quickly, after n moves, there will be m subtrees
    n = 1, m = 20
    n = 2, m = 400
    n = 3, m = 8902
    n = 4, m = 197281
    ...
    """
    if d == 0 or board.outcome() is not None:
        return ChessTree(board, evaluate_board(board))

    chess_tree = ChessTree(board, 0)
    legal_moves = board.generate_legal_moves()

    if board.turn:  # evaluates to true if the player to move is white
        # Thus, they are trying to maximize the evaluation value.
        for move in legal_moves:
            board.push(move)
            subtree = generate_chess_tree(board, d - 1)
            chess_tree.add_subtree(subtree)
            board.pop()

        if chess_tree.get_subtrees():
            chess_tree.eval_position = max(subtree.eval_position for subtree in chess_tree.get_subtrees())

    else:  # it is black's turn, thus, they are trying to minimize the evaluation value.
        for move in legal_moves:
            board.push(move)
            subtree = generate_chess_tree(board, d - 1)
            chess_tree.add_subtree(subtree)
            board.pop()

        if chess_tree.get_subtrees():
            chess_tree.eval_position = min(subtree.eval_position for subtree in chess_tree.get_subtrees())

    return chess_tree


def generate_pruned_chess_tree(board: chess.Board, d: int, alpha: float, beta: float) -> ChessTree:
    """Generate a pruned chess tree of depth d for all valid moves from the current board using the
    alpha beta pruning algorithm. This prunes branches of trees that do not need to be computed because
    previous branches in the tree have a better evaluation score.

    For the returned ChessTree:
        - Its board is the given board.
        - It contains all possible move sequences of length <= d from the board.
        - If d == 0, a size-one ChessTree is returned.

    Generally, if we attempt sort the moves from best to worst, this function will be able to prune more trees.
    By just computing the unsorted list of legal_moves, we expect after n moves, there will be m subtrees:
    n = 1, m = 20
    n = 2, m = 58
    n = 3, m = 347
    n = 4, m = 2024
    ...

    However, if we sort by using the get_order_moves() function, after n moves, there will be m subtrees:
    n = 1, m = 20
    n = 2, m = 88
    n = 3, m = 81
    n = 4, m = 1277
    """
    if d == 0 or board.outcome() is not None:
        return ChessTree(board, search_all_captures(board, alpha, beta))

    chess_tree = ChessTree(board, 0)
    legal_moves = get_ordered_moves(board)

    if board.turn:  # evaluates to true if the player to move is white
        # Thus, they are trying to maximize the evaluation value.
        for move in legal_moves:
            board.push(move)
            subtree = generate_pruned_chess_tree(board, d - 1, alpha, beta)
            evaluation = subtree.eval_position
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                board.pop()
                break
            else:  # if the loop is not broken out of, we can add the subtree into the chess tree
                chess_tree.add_subtree(subtree)
                board.pop()

        if chess_tree.get_subtrees():
            chess_tree.eval_position = max(subtree.eval_position for subtree in chess_tree.get_subtrees())

    else:  # it is black's turn, thus, they are tyring to minimize the evaluation value.
        for move in legal_moves:
            board.push(move)
            subtree = generate_pruned_chess_tree(board, d - 1, alpha, beta)
            evaluation = subtree.eval_position
            beta = min(beta, evaluation)
            if beta <= alpha:
                board.pop()
                break
            else:  # if the loop as not been broken out of, the subtree cannot be pruned
                chess_tree.add_subtree(subtree)
                board.pop()

        if chess_tree.get_subtrees():
            chess_tree.eval_position = min(subtree.eval_position for subtree in chess_tree.get_subtrees())

    return chess_tree


################################################################################
# Searching functions
################################################################################
def search(board: chess.Board, d: int, alpha: float, beta: float) -> float:
    """Traverse through the given chess board by looking into each legal move up to a depth of d.
    Use alpha-beta pruning to skip over some moves after finding better moves previously.
    Return the evaluation of the best move that was found.

    Does not use computational resources to compute a tree but instead just travels through the board
    as if it was a tree.
    """
    if d == 0 or board.outcome() is not None:
        # we don't want to end the search abruptly when d is 0, instead, look at all captures that follow to see
        # if the true value of the position after all the captures are made
        return search_all_captures(board, alpha, beta)
        # return evaluate_board(board)
    else:
        # legal_moves = board.generate_legal_moves()
        legal_moves = get_ordered_moves(board)
        if board.turn:
            max_evaluation = -math.inf
            for move in legal_moves:
                if move.promotion is not None and move.promotion != chess.QUEEN:
                    continue  # we want to skip any promotion move that is not to a queen
                board.push(move)
                evaluation = search(board, d - 1, alpha, beta)
                board.pop()
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_evaluation
        else:
            min_evaluation = math.inf
            for move in legal_moves:
                if move.promotion is not None and move.promotion != chess.QUEEN:
                    continue  # we want to skip any promotion move that is not to a queen
                board.push(move)
                evaluation = search(board, d - 1, alpha, beta)
                board.pop()
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_evaluation


def search_all_captures(board: chess.Board, alpha: float, beta: float) -> float:
    """Return a float representing the evaluation of the board after all possible captures are made."""
    evaluation = evaluate_board(board)
    if evaluation >= beta:
        return beta
    alpha = max(alpha, evaluation)

    capture_moves = [move for move in board.generate_legal_moves() if board.is_capture(move)]

    for move in capture_moves:
        board.push(move)
        evaluation = search_all_captures(board, -beta, -alpha)
        board.pop()

        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)

    return alpha


def find_move_by_search(board: chess.Board, d: int):
    """Returns the best move that leads to the best position after a depth of d, given a chess board
    according to the search algorithm."""
    if board.turn:
        best_move_eval = -math.inf
    else:
        best_move_eval = math.inf

    # legal_moves = board.generate_legal_moves()
    legal_moves = get_ordered_moves(board)
    best_move_found = chess.Move.null()

    for move in legal_moves:
        board.push(move)
        evaluation = search(board, d - 1, -math.inf, math.inf)
        board.pop()
        if board.turn and evaluation >= best_move_eval:
            best_move_eval = evaluation
            best_move_found = move
        elif not board.turn and evaluation <= best_move_eval:
            best_move_eval = evaluation
            best_move_found = move

    return best_move_found


def get_ordered_moves(board: chess.Board) -> list[chess.Move]:
    """For a given board in chess, attempt to order the legal moves from best to worst
     by evaluating each move by evaluate_move."""
    # sort in descending order from highest eval to lowest eval if the turn is White, reversed if black
    moves = sorted(board.generate_legal_moves(), key=lambda move: evaluate_move(board, move), reverse=board.turn)
    return list(moves)


################################################################################
# Functions for evaluating boards, moves, pieces
################################################################################
def evaluate_move(board: chess.Board, move: chess.Move) -> float:
    """Evaluates a move on how good it is. Generally, a piece with less value capturing a piece with higher value
    is a good move, the other way around is bad. This will always give promotion to queen a high evaluation.

    On a side note, sometimes, promoting to a queen is not the best because it can lead to a situation where the
    opposing king is in stalemate. But that is beyond the scope of this program, it perhaps can be implemented
    in future additions.
    """
    if move.promotion == chess.QUEEN:
        if board.turn:
            return math.inf
        else:
            return -math.inf
    elif move.promotion is not None:  # we want to discourage promotion to anything other than queen
        if board.turn:
            return -math.inf
        else:
            return math.inf

    piece = board.piece_at(move.from_square)
    before_move_evaluation = evaluate_piece(piece, move.from_square)
    after_move_evaluation = evaluate_piece(piece, move.to_square)
    position_change = after_move_evaluation - before_move_evaluation

    # check if move was a capture
    if board.is_capture(move):
        if board.is_en_passant(move):
            capture_evaluation = piece_vals[chess.PAWN]
        else:
            capture_evaluation = piece_vals[board.piece_at(move.to_square).piece_type] - \
                                 piece_vals[board.piece_at(move.from_square).piece_type]
    else:
        capture_evaluation = 0

    evaluation = position_change + capture_evaluation
    if board.turn:
        return evaluation
    else:
        return -evaluation


def evaluate_piece(piece: chess.Piece, square: chess.Square) -> float:
    """Returns an evaluation of a piece on a specific square based on the bonus tables.
    Positive if the piece is White, negative if piece is black.
    """
    if piece.color == chess.WHITE:
        if piece.piece_type == chess.PAWN:
            s = piece_vals[chess.PAWN] + pawns_table_w[square]
        elif piece.piece_type == chess.KNIGHT:
            s = piece_vals[chess.KNIGHT] + knights_table_w[square]
        elif piece.piece_type == chess.ROOK:
            s = piece_vals[chess.ROOK] + rooks_table_w[square]
        elif piece.piece_type == chess.QUEEN:
            s = piece_vals[chess.QUEEN] + queens_table_w[square]
        else:
            s = piece_vals[chess.KING] + kings_table_w[square]
    else:
        if piece.piece_type == chess.PAWN:
            s = -piece_vals[chess.PAWN] - pawns_table_b[square]
        elif piece.piece_type == chess.KNIGHT:
            s = -piece_vals[chess.KNIGHT] - knights_table_b[square]
        elif piece.piece_type == chess.ROOK:
            s = -piece_vals[chess.ROOK] - rooks_table_b[square]
        elif piece.piece_type == chess.QUEEN:
            s = -piece_vals[chess.QUEEN] - queens_table_b[square]
        else:
            s = -piece_vals[chess.KING] - kings_table_b[square]
    return s


def evaluate_board(board: chess.Board) -> float:
    """Return an evaluation of the board based on piece material and position bonuses."""
    final = 0
    if board.outcome() is not None:
        if board.is_checkmate():
            if board.turn:
                return -math.inf
            else:
                return math.inf
        elif board.is_stalemate():
            return 0
        elif board.is_insufficient_material():
            return 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            final += evaluate_piece(piece, square)

    return final
