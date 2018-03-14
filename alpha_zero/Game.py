from typing import Tuple, List

from alpha_zero.Player import Player
from alpha_zero.Board import Board


class Game():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        pass

    def getInitBoard(self) -> Board:
        """
        :returns: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        pass

    def getBoardSize(self) -> Tuple[int,int]:
        """
        :returns: (x,y): a tuple of board dimensions
        """
        pass

    def getActionSize(self) -> int:
        """
        :returns: number of all possible actions
        """
        pass

    def getNextState(self, board: Board, player: int, action) -> Tuple[Board,int]:
        """
        :param board: current board
        :param player: current player (1 or -1)
        :param action: action taken by current player

        :returns: nextBoard: board after applying action. Must be a copy of the input board
        :returns: nextPlayer: player who plays in the next turn (should be -player)
        """
        pass

    def getValidMoves(self, board: Board, player: int) -> List[int]:
        """

        :param board: current board
        :param player: current player

        :returns: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        pass

    def getGameEnded(self, board: Board, player: int) -> float:
        """

        :param board: current board
        :param player: current player (1 or -1)

        :returns: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        pass

    def getCanonicalForm(self, board: Board, player: int) -> Board:
        """

        :param board: current board
        :param player: current player (1 or -1)

        :returns: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        pass

    def getSymmetries(self, board: Board, pi):
        """

        :param board: current board
        :param pi: policy vector of size self.getActionSize()

        :returns: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        pass

    def stringRepresentation(self, board: Board) -> str:
        """

        :param board: current board

        :returns: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        pass
