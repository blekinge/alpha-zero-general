from typing import List

import numpy as np
from colorama import Fore, Style

from quatro.QuatroBoard import Board


def display(board: Board):

    # board = Board(board_state=board_state)

    n = board.n
    piece_to_deploy = board.selected_piece
    # piece_to_deploy = piece_to_deploy - (1 << (n))

    print("Piece to deploy: ")
    piece_bit4 = bit(piece_to_deploy,3)
    print(Fore.BLUE+'{0:01b}'.format(piece_bit4), end="")

    piece_bit3 = bit(piece_to_deploy,2)
    print(Fore.BLUE+'{0:01b}'.format(piece_bit3), end="")
    print(Style.RESET_ALL, end="")
    print("")

    piece_bit2 = bit(piece_to_deploy,1)
    print(Fore.BLUE+'{0:01b}'.format(piece_bit2), end="")

    piece_bit1 = bit(piece_to_deploy,0)
    print(Fore.BLUE+'{0:01b}'.format(piece_bit1), end="")
    print(Style.RESET_ALL, end="")
    print("")

    print("   ", end=" ")
    for y in range(n):
        print(y, " ", end="")
    print("")

    print("  ", end="")
    for _ in range(n):
        print("--", end="-")
    print("-")

    #

    for y in range(n):

        print(y, "|", end="")  # print the row #
        for x in range(n):
            piece = board[x][y]  # get the piece to print
            if piece != 0:
                print('{0:01b}'.format(bit(piece, 3)), end="")
                print('{0:01b}'.format(bit(piece, 2)), end="")
            else:
                print("  ", end="")
            if x != n-1:
                print("|", end="")
        print("|")

        print("  |", end="")
        for x in range(n):
            piece = board[x][y]  # get the piece to print
            if piece != 0:
                print('{0:01b}'.format(bit(piece,1)), end="")
                print('{0:01b}'.format(bit(piece,0)), end="")
            else:
                print("  ", end="")
            if x != n-1:
                print("|", end="")
        print("|")

        if y != n-1:
            print("  |", end="")
            for x in range(n):
                if x != n-1:
                    print("---", end="")
                else:
                    print("--|")


    print("  ", end="")
    for _ in range(n):
        print("--", end="-")
    print("-")
    print(list(map(lambda piece: '{0:04b}'.format(piece & 0b1111),board.remaining_pieces)))


def bit(piece_to_deploy, startBit: int, endBit:int=None):

    mask = (1 << startBit)
    i = (piece_to_deploy & mask)
    return i >> startBit


