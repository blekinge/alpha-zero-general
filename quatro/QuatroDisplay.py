import numpy as np
from colorama import Fore, Style

from quatro.QuatroBoard import QuatroBoard, Piece


def display(board_state: np.ndarray):
    n = board_state.shape[0]
    board = QuatroBoard(n, board_state=board_state)

    piece_to_deploy = board.selected_piece
    # piece_to_deploy = piece_to_deploy - (1 << (n))

    if len(board.empty_tiles) > 0:
        print("Piece to deploy: ")
        print(Fore.BLUE + '{0:01b}'.format(piece_to_deploy[0]), end="")

        print(Fore.BLUE + '{0:01b}'.format(piece_to_deploy[1]), end="")
        print(Style.RESET_ALL, end="")
        print("")

        print(Fore.BLUE + '{0:01b}'.format(piece_to_deploy[2]), end="")

        print(Fore.BLUE + '{0:01b}'.format(piece_to_deploy[3]), end="")
        print(Style.RESET_ALL, end="")
        print("")

    print("   ", end=" ")
    mid = (n - 1) / 2
    for y in range(n):
        if y == mid: continue
        if y < mid:
            print(chr(ord('a') + y)," ", end="")
        else:
            print(chr(ord('a') + y-1), " ", end="")
        # print(y, " ", end="")
    print("")

    print("  ", end="")
    for y in range(n):
        if y == mid: continue
        print("--", end="-")
    print("-")

    #

    for x in range(n):
        if x == mid: continue
        if x < mid:
            print(x, "|", end="")  # print the row #
        else:
            print(x-1, "|", end="")  # print the row #
        for y in range(n):
            if y == mid: continue
            piece = Piece(board[x][y])  # get the piece to print
            if piece is not None:
                print('{0:01b}'.format(piece[0]), end="")
                print('{0:01b}'.format(piece[0]), end="")
            else:
                print("  ", end="")
            if y != n-1:
                print("|", end="")
        print("|")

        print("  |", end="")
        for y in range(n):
            if y == mid: continue
            piece = Piece(board[x][y])  # get the piece to print
            if piece is not None:
                print('{0:01b}'.format(piece[2]), end="")
                print('{0:01b}'.format(piece[3]), end="")
            else:
                print("  ", end="")
            if y != n-1:
                print("|", end="")
        print("|")

        if x != n-1:
            print("  |", end="")
            for y in range(n):
                if y == mid: continue
                if y != n-1:
                    print("---", end="")
                else:
                    print("--|")


    print("  ", end="")
    for y in range(n):
        if y == mid: continue
        print("--", end="-")
    print("-")

    print("Remaining pieces: ",end="")
    print(str(board.remaining_pieces))



