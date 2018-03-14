import numpy as np

from alpha_zero.MCTS import MCTS
from .QuatroBoard import QuatroBoard
from .quatro_keras.NNet import NNetWrapper as KerasNNet


"""
Random and Human-ineracting players for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board: QuatroBoard):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())

        print(f"Taking action {a} = "+ self.game.prettyprint_action(a))
        return a


class HumanPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board: QuatroBoard):
        valid = self.game.getValidMoves(board, 1)
        mid = (self.game.n -1) / 2
        while True:

            # Python 3.x
            a = input("letter number piece: ")
            # Python 2.x
            # a = raw_input()

            coordinates = a.split(' ')

            x = ord(coordinates[0])-ord('a')
            if x >= mid:
                x += 1
            print(f"effective x={x}")

            y = int(coordinates[1])
            if y >= mid:
                y += 1
            print(f"effective y={y}")

            piece = int(coordinates[2], 2)

            a = self.game.encodeAction((y, x, piece)) if x != -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a



class KerasNeuralNetPlayer():
    def __init__(self, game, args1) -> None:
        # nnet players
        self.game = game
        neural_net_1 = KerasNNet(game)
        self.mcts1 = MCTS(game, neural_net_1, args1)
        # n1.load_checkpoint('./pretrained_models/tictactoe/keras/','best-25eps-25sim-10epch.pth.tar')

    def play(self, board: QuatroBoard):
        return np.argmax(self.mcts1.getActionProb(board, temperature=0))
