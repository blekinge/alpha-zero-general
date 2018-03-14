from colorama import Fore, Style

from quatro.QuatroBoard import QuatroBoard


def display(board: QuatroBoard):

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
            piece = board[x][y]  # get the piece to print
            if piece != 0:
                print('{0:01b}'.format(bit(piece, 3)), end="")
                print('{0:01b}'.format(bit(piece, 2)), end="")
            else:
                print("  ", end="")
            if y != n-1:
                print("|", end="")
        print("|")

        print("  |", end="")
        for y in range(n):
            if y == mid: continue
            piece = board[x][y]  # get the piece to print
            if piece != 0:
                print('{0:01b}'.format(bit(piece,1)), end="")
                print('{0:01b}'.format(bit(piece,0)), end="")
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
    print(list(map(lambda piece: '{0:04b}'.format(piece & 0b1111),board.remaining_pieces)))


def bit(piece_to_deploy, startBit: int, endBit:int=None):

    mask = (1 << startBit)
    i = (piece_to_deploy & mask)
    return i >> startBit


