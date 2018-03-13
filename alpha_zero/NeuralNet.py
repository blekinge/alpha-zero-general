from typing import List, Tuple

import numpy as np

from alpha_zero.Board import Board


class NeuralNet():
    """
    This class specifies the base NeuralNet class. To define your own neural
    network, subclass this class and implement the functions below. The neural
    network does not consider the current player, and instead only deals with
    the canonical form of the board.

    See othello/NNet.py for an example implementation.
    """

    def __init__(self, game):
        pass

    def train(self, examples: List[Tuple[Board,List[float],List[int]]]):
        """
        This function trains the neural network with examples obtained from
        self-play.

        :param examples: a list of training examples, where each example is of form
                      (board, pi, v). pi is the MCTS informed policy vector for
                      the given board, and v is its value. The examples has
                      board in its canonical form.
        """
        pass

    def predict(self, board: Board) -> Tuple[np.array,float]:
        """
        :param board: current board in its canonical form.

        :returns pi: a policy vector for the current board- a numpy array of length game.getActionSize
        :returns v: a float in [-1,1] that gives the value of the current board
        """
        pass

    def save_checkpoint(self, folder: str, filename:str):
        """
        Saves the current neural network (with its parameters) in
        folder/filename
        """
        pass

    def load_checkpoint(self, folder: str, filename:str):
        """
        Loads parameters of the neural network from folder/filename
        """
        pass
