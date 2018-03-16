from __future__ import print_function

import sys
from typing import Tuple, List

from alpha_zero.Player import Player
from alpha_zero.Game import Game

sys.path.append('..')
from .QuatroBoard import QuatroBoard, Piece
import numpy as np

from colorama import init
init()




"""
Game class implementation for the game of Quatro
Based on the TicTacToeGame
Based on the OthelloGame by Surag Nair.
"""


class QuatroGame(Game):

    def __init__(self, n:int=5):
        self.n = n


    def getInitBoard(self) -> np.array:
        # return initial board (numpy board)
        b = QuatroBoard(self.n)
        return b.state

    def getBoardSize(self) -> Tuple[int, int]:
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self) -> int:
        # return number of actions
        # TODO in terms of n
        return (1 << (2 + 2 + self.n-1)) + 1

    def getNextState(self, board_state: np.ndarray, player: int, action: int) -> Tuple[np.ndarray, int]:
        """
        if player takes action on board, return next (board_state,player)
        :param board_state: current board state
        :param player: current player (1 or -1)
        :param action: action taken by current player

        :return nextBoard: board_state after applying action
        :return nextPlayer: player who plays in the next turn (should be -player)
        """
        board = QuatroBoard(self.n, np.copy(board_state))
        #
        # if action == self.getActionSize()-1 :
        #     # Means no pieces left, so just place the last piece
        #     piece = board.selected_piece
        #     x,y = board.empty_tiles[0]
        # else:
        x, y, piece = self.decodeAction(action)

        if len(board.remaining_pieces)==0 and len(board.empty_tiles)==1:
            pass
            # print("Placing last piece")
        else:
            if piece in board.used_pieces or piece == board.selected_piece:
                print("invalid state")
                # Invalid, so your turn again
                return board_state, player

        # Perform the move
        board.execute_move((x,y,piece), player)

        # Next turn
        return board.state, -player


    # This returns array of the actions that are fed into getNextState
    def getValidMoves(self, board_state: np.ndarray, player: int):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()

        board = QuatroBoard(n=self.n, board_state=board_state)

        legalMoves = board.get_legal_moves(player)

        # Means place last piece and end
        if len(legalMoves) == 0:
            x,y = board.empty_tiles[0]
            p = board.selected_piece
            valids[self.encodeAction((x, y, p))] = 1
            return np.array(valids)

        for x, y, p in legalMoves:
            action = self.encodeAction((x, y, p))
            valids[action] = 1
        return valids


    def getGameEnded(self, board_state: np.ndarray, player: int) -> int:
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        board = QuatroBoard(self.n, board_state)

        if board.is_win(player):
            return player
        if board.has_legal_moves():
            return 0
        # draw has a very little value 
        return 1e-4

    def getCanonicalForm(self, board_state: np.ndarray, player: int) -> np.ndarray:
        # return state if player==1, else return -state if player==-1
        return board_state

    def getSymmetries(self, board_state: np.array, action_prop_vector: List[float]):
        assert (len(action_prop_vector) == self.getActionSize())  # 1 for pass
        pi_board = np.reshape(action_prop_vector[:-1], ((self.n - 1) ** 2, (self.n - 1) ** 2))
        symmetrics = []

        # mirror, rotational
        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board_state, i)
                newPi = np.rot90(pi_board, i)
                if+ j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)


                symmetrics += [(newB, list(newPi.ravel()) + [action_prop_vector[-1]])]

        return symmetrics

    def stringRepresentation(self, board_state: np.array):
        return board_state.tostring()

    def encodeAction(self, action: Tuple[int, int, Piece]) -> int:
        x, y, piece = action

        if x > 1: x -= 1
        if y > 1: y -= 1

        moveMask = self.n - 2
        n_x = (x & moveMask) << (self.n-1 + 2)
        n_y = (y & moveMask) << (self.n-1)
        return n_x + n_y + (piece.toInt())

    def decodeAction(self, encoded_action: int) -> Tuple[int, int, Piece]:

        propertyMask = (self.n -1)**2 -1

        x = (encoded_action >> (self.n-1 + 2)) & 0b11
        if x > 1: x +=1
        y = (encoded_action >> (self.n-1)) & 0b11
        if y > 1: y += 1
        piece = Piece.fromInt(encoded_action & propertyMask)
        return x, y, piece