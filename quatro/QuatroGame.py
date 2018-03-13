from __future__ import print_function

import sys
from typing import Tuple, List

sys.path.append('..')
from Game import Game
from .QuatroBoard import Board
import numpy as np
import copy

from colorama import Fore, Back, Style
from colorama import init
init()




"""
Game class implementation for the game of Quatro
Based on the TicTacToeGame
Based on the OthelloGame by Surag Nair.
"""


class QuatroGame(Game):

    def __init__(self, n:int=4):
        self.n = n


    def getInitBoard(self) -> Board:
        # return initial board (numpy board)
        b = Board(self.n)
        self.property_mask = b.property_mask
        self.is_set_mask = b.is_set_mask
        return b

    def getBoardSize(self) -> Tuple[int, int]:
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self) -> int:
        # return number of actions
        # TODO in terms of n
        return (1 << (2 + 2 + self.n)) + 1

    def getNextState(self, board: Board, player: int, action: int) -> Tuple[Board, int]:
        """
        if player takes action on board, return next (board_state,player)
        :param board_state: current board state
        :param player: current player (1 or -1)
        :param action: action taken by current player

        :return nextBoard: board_state after applying action
        :return nextPlayer: player who plays in the next turn (should be -player)
        """
        # board = Board(self.n, np.copy(board_state))

        if action == self.getActionSize()-1 :
            # Means no pieces left, so just place the last piece
            piece = board.selected_piece
            x,y = board.empty_tiles[0]
        else:
            x, y, piece = self.decodeAction(action)

            if piece in board.used_pieces or piece == board.selected_piece:
                print("invalid state")
                # Invalid, so your turn again
                return board, player

        # Perform the move
        board.execute_move((x,y,piece), player)

        # Next turn
        return board, -player


    # This returns array of the actions that are fed into getNextState
    def getValidMoves(self, board: Board, player: int):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()

        # board = Board(n=self.n, board_state=board_state)

        legalMoves = board.get_legal_moves(player)

        # Means place last piece and end
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)

        for x, y, p in legalMoves:
            move = (x,y,p)
            action = self.encodeAction(move)
            valids[action] = 1
        return np.array(valids)


    def getGameEnded(self, board: Board, player: int) -> int:
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        # board = Board(self.n, board_state)

        if board.is_win(player):
            return 1
        if board.has_legal_moves():
            return 0
        # draw has a very little value 
        return 1e-4

    def getCanonicalForm(self, board: Board, player: int):
        # return state if player==1, else return -state if player==-1
        return board

    def getSymmetries(self, board: Board, pi: List[float]):
        return [board]
        # # mirror, rotational
        # assert (len(pi) == self.getActionSize())  # 1 for pass
        # pi_board = np.reshape(pi[:-1], (self.n ** 2, self.n ** 2))
        # l = []
        #
        # for i in range(1, 5):
        #     for j in [True, False]:
        #         newB = np.rot90(board.state, i)
        #         newPi = np.rot90(pi_board, i)
        #         if j:
        #             newB = np.fliplr(newB)
        #             newPi = np.fliplr(newPi)
        #         l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        # return l

    def stringRepresentation(self, board: Board):
        # 8x8 numpy array (canonical board)
        return board.state.tostring()

    def encodeAction(self, action: Tuple[int, int, int]) -> int:
        x, y, p = action
        # x,y is 0-3, so 2 bits.
        # p is 5 bits
        # p = p - 0b10000
        n_x = (x & 0b11) << (self.n + 2)
        n_y = (y & 0b11) << (self.n)
        return n_x + n_y + (p & self.property_mask)

    def decodeAction(self, encoded_action: int) -> Tuple[int, int, int]:

        x = (encoded_action >> (self.n + 2)) & 0b11
        y = (encoded_action >> (self.n)) & 0b11
        piece = (encoded_action & self.property_mask) + self.is_set_mask

        return x, y, piece

    def prettyprint_action(self, encoded_action: int):
        x,y,p = self.decodeAction(encoded_action)
        return f"({x},{y},"+'{0:04b}'.format(p & self.property_mask)+")"