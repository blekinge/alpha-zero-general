import numpy as np

from alpha_zero.Player import Player
from alpha_zero.Board import Board
from alpha_zero.MCTS import MCTS
from tictactoe.tictactoe_keras.NNet import NNetWrapper as KerasNNet


"""
Random and Human-ineracting players for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer(Player):
    def __init__(self, game, name):
        super().__init__(name)
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanPlayer(Player):
    def __init__(self, game, name):
        super().__init__(name)
        self.game = game


    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        # for i in range(len(valid)):
        #     if valid[i]:
        #         print(int(i/self.game.n), int(i%self.game.n))
        while True:
            print("Make your move!")
            # Python 3.x
            a = input("letter number: ")
            # Python 2.x 
            # a = raw_input()
            coordinates = a.split(' ')
            x = ord(coordinates[0])-ord('a')
            y = int(coordinates[1])
            # x,y = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x!= -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a

class KerasNeuralNetPlayer(Player):
    def __init__(self, game, args1, name) -> None:
        # nnet players
        super().__init__(name)
        self.game = game
        self.neural_net_1 = KerasNNet(game)
        self.mcts1 = MCTS(game, self.neural_net_1, args1)

    def load_brain(self, folder:str, file:str):
        self.neural_net_1.load_checkpoint('./pretrained_models/tictactoe/keras/','best-25eps-25sim-10epch.pth.tar')

    def play(self, board: Board):
        return np.argmax(self.mcts1.getActionProb(board, temperature=0))
