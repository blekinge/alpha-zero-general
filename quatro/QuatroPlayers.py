from typing import Tuple

import numpy as np

from .QuatroGame import QuatroGame
from alpha_zero.Player import Player
from alpha_zero.MCTS import MCTS
from .QuatroBoard import QuatroBoard, Piece
from .quatro_keras.NNet import NNetWrapper as KerasNNet


"""
Random and Human-ineracting players for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer(Player):
    def __init__(self, game: QuatroGame, name:str):
        super().__init__(name)
        self.game = game

    def play(self, board_state: np.array):
        board = QuatroBoard(self.game.n,board_state=board_state)
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board_state, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())

        display_action=human_decode(self.game, a)
        print(f"{self.name} placed {board.selected_piece} in '{display_action[1]} {display_action[0]}' and gives you {display_action[2]}")

        return a


def human_decode(game: QuatroGame, encoded_action: int)->Tuple[int,chr,Piece]:
    mid = (game.n - 1) / 2

    x,y,piece = game.decodeAction(encoded_action)
    if x >= mid:
        x -= 1
    if y >= mid:
        y -= 1
    y = chr(ord('a') + y)
    return x, y, piece


class HumanPlayer(Player):
    def __init__(self, game: QuatroGame, name:str):
        super().__init__(name)
        self.game = game

    def play(self, board_state: np.ndarray):
        valid = self.game.getValidMoves(board_state, 1)
        mid = (self.game.n -1) / 2
        while True:

            # Python 3.x
            a = input("letter number piece: ")
            # Python 2.x
            # a = raw_input()
            a = a.strip()
            coordinates = a.split(' ')

            x = ord(coordinates[0])-ord('a')
            if x >= mid:
                x += 1
            print(f"effective x={x}")

            y = int(coordinates[1])
            if y >= mid:
                y += 1
            print(f"effective y={y}")

            piece = Piece.fromNP(int(coordinates[2], 2))

            a = self.game.encodeAction((y, x, piece)) if x != -1 else self.game.n ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a



class KerasNeuralNetPlayer(Player):
    def __init__(self, game: QuatroGame, args1, name:str) -> None:
        # nnet players
        super().__init__(name)
        neural_net_1 = KerasNNet(game)
        self.mcts1 = MCTS(game, neural_net_1, args1)
        # n1.load_checkpoint('./pretrained_models/tictactoe/keras/','best-25eps-25sim-10epch.pth.tar')

    def play(self, board: QuatroBoard):
        return np.argmax(self.mcts1.getActionProb(board, temperature=0))
