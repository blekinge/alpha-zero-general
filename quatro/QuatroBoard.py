'''
Board class for the game of Quatro.
Default board size is 4x4.
Board data:
  16 pieces = 10000,10001,10010,10011,10100,10101,10110,10111,11000,11001,11010,11011,11100,11101,11110,11111
  0=empty
  the format is binary
  color(black/white) ,height(tall/short), shape(round/square), surface(holed/smooth)
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[3][3] is the bottom right square,
Squares are stored and manipulated as (x,y) tuples.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the board for the game of Othello by Eric P. Nichols.

'''

# from bkcharts.attributes import color
from typing import List, Tuple

import numpy as np

from alpha_zero.Board import Board


def allset(values: List[int]):
    from functools import reduce
    product = reduce((lambda x, y: x * y), values)
    return product > 0


class QuatroBoard(Board):
    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, n=5, board_state:np.array = None):
        "Set up initial board configuration."

        self.n = n

        # 0b10000
        self.is_set_mask = 1 << (self.n-1)

        # 0b01111
        self.property_mask = (1 << (self.n-1)) - 1
        self.mid = int((self.n-1)/2)

        if board_state is None:
            # Create the empty board array (5 x 5). The only 4 x 4 is needed, but the center is the selected piece
            tiles = [None] * (self.n)
            for i in range(self.n):
                tiles[i] = [0] * (self.n)
            self._tiles = np.array(tiles, dtype=int)
            # Select the first piece per default
            self._tiles[self.mid][self.mid] = 0 + self.is_set_mask
            # selected_piece = 0 + self.is_set_mask
        else:
            self._tiles = board_state


    @property
    def state(self) -> np.array:
        return self._tiles

    # add [][] indexer syntax to the Board
    def __getitem__(self, index) -> List[int]:
        return self._tiles[index]

    @property
    def selected_piece(self) -> int:
        return self[self.mid][self.mid]

    @selected_piece.setter
    def selected_piece(self, piece: int) -> None:
        self._tiles[self.mid][self.mid] = piece

    @property
    def used_pieces(self):
        used_pieces = [self[x][y] for x in range(self.n) for y in range(self.n) if self[x][y] != 0 and x != self.mid and y != self.mid]
        used_pieces.append(self.selected_piece)
        return used_pieces

    @property
    def remaining_pieces(self):
        used_pieces = self.used_pieces
        remaining_pieces = [p
                            for p in range(self.is_set_mask, (self.n-1) * (self.n-1) + self.is_set_mask)
                            if p not in used_pieces]
        return remaining_pieces

    @property
    def empty_tiles(self) -> List[Tuple[int, int]]:
        empty_tiles = [(x, y) for x in range(self.n) for y in range(self.n) if self[x][y] == 0 and x != self.mid and y != self.mid]
        return empty_tiles

    def get_legal_moves(self, color: int) -> List[Tuple[int, int, int]]:
        """Returns all the legal moves for the given color.
        A move consist of placing the selected piece and selecting a new piece for your opponent

        @param color not used and came from previous version.

        The result is a triplet (x,y,p), x+y to specify where to place the selected piece and a piece to make
        the new selected piece
        """
        remaining_pieces = self.remaining_pieces

        empty_tiles = self.empty_tiles

        legal_moves = [(x, y, p) for x, y in empty_tiles for p in remaining_pieces]
        return legal_moves

    def has_legal_moves(self):
        return len(self.empty_tiles) != 0


    def is_win(self, player: int):
        """Check whether the given player has collected a Quadlet in any direction;
        @param player (1=white,-1=black)
        """

        for y in range(self.n):
            if y == self.mid: continue
            y_strip = [self[x][y] for x in range(self.n) if x != self.mid]
            # y_strip = self[:, y]

            if self.check_strip(y_strip):
                return True

        for x in range(self.n):
            if x == self.mid: continue
            x_strip = [self[x][y] for y in range(self.n) if y != self.mid]

            # x_strip = self[x, :]
            if self.check_strip(x_strip):
                return True

        d1_strip = [self[d][d] for d in range(self.n) if d != self.mid]
        if self.check_strip(d1_strip):
            return True

        d2_strip = [self[d][-d] for d in range(self.n) if d != self.mid]
        if self.check_strip(d2_strip):
            return True

        return False

    def execute_move(self, move: Tuple[int, int, int], player: int):
        """Perform the given move on the board; 
        """

        (x, y, p) = move

        # Add the piece to the empty square.
        assert self[x][y] == 0
        assert p > 0
        assert x != self.mid
        assert y != self.mid

        # print(f"Placing {(self.selected_piece & 0b1111):04b} at {x},{y}")
        self[x][y] = self.selected_piece  # +(1<<self.n)

        self.selected_piece = p
        # print(f"Selecting {(self.selected_piece & 0b1111):04b} for opponent\n")

    def check_strip(self, strip: List[int]):

        # 0b01111
        count = self.property_mask
        for value in strip:
            if value & self.is_set_mask == 0:
                count = 0
                break
            # The first 4 bits are the properties, so AND those out
            properties = (value & self.property_mask)
            # Then AND with the collected properties so far
            count = count & properties
            # If there is no overlap, stop this
            if count == 0:
                break
        # If there is still overlap after we went through the strip, we have a winner
        if count > 0:
            return True

        count = self.property_mask
        for value in strip:
            if value & self.is_set_mask == 0:
                count = 0
                break
            # The first 4 bits are the properties, so AND those out
            properties = (~value & self.property_mask)
            # Then AND with the collected properties so far
            count = count & properties
            # If there is no overlap, stop this
            if count == 0:
                break
        # If there is still overlap after we went through the strip, we have a winner
        return count > 0
