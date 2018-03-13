import numpy as np

from quatro.QuatroBoard import Board

"""
Random and Human-ineracting players for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board: Board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())

        print(f"Taking action {a} = "+ self.game.prettyprint_action(a))
        return a


class HumanQuatroPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board: Board):
        # Board or board_state
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        # for i in range(len(valid)):
        #     if valid[i]:
        #         print(decodeAction(i))
        #         # print(int(i/self.game.n), int(i%self.game.n))
        while True:

            # Python 3.x
            a = input("x y bbbb: ")
            # Python 2.x 
            # a = raw_input()
            params = a.split(' ')
            x = int(params[0])
            y = int(params[1])
            piece = int(params[2], 2)

            a = self.game.encodeAction((x, y, piece)) if x != -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a
