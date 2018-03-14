def display(board):
    n = board.shape[0]

    print("   ", end="")
    for y in range(n):
        print(chr(ord('a') + y),"", end="")
    print("")
    print("  ", end="")
    for _ in range(n):
        print ("-", end="-")
    print("--")
    for x in range(n):
        print(x, "|",end="")    # print the row #
        for y in range(n):
            piece = board[y][x]    # get the piece to print
            if piece == -1: print("X ",end="")
            elif piece == 1: print("O ",end="")
            else:
                if x==n:
                    print("-",end="")
                else:
                    print("- ",end="")
        print("|")

    print("  ", end="")
    for _ in range(n):
        print ("-", end="-")
    print("--")