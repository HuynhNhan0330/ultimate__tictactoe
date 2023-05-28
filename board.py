import copy

from const import *

from board_dim import BoardDim


class Board:
    """
    Class Board
    Board tictactoe
    """

    def __init__(self, dims=None, linewidth=10, margin=21, sub=False):
        """
        Constructor
        :param dims: object BoardDim (board_dim.py)
        :param linewidth: Width line
        :param margin: margin board
        :param sub: sub board?
        """
        self.dims = dims
        self.linewidth = linewidth
        self.margin = margin
        self.sub = sub

        if not dims:
            self.dims = BoardDim(SIZE_BOARD, SIZE_BOARD, margin, margin)

        self.squares = [[2, 2, 2] for row in range(DIM)]  # List squares
        self.offset = self.dims.sqsize * 0.2
        self.radius = (self.dims.sqsize // 2) * 0.7  # Radius draw O
        self.value = 2
        self.valid_col = 1
        self.valid_row = 1

        if not sub:
            self.create_ultimate()

    def __str__(self):
        """
        String object
        :return: board string form
        """
        out = [[' ' if j != 3 and j != 7 else '#' for i in range(17)] for j in range(11)]
        for row in range(9):
            for col in range(9):
                sqr = self.squares[row // 3][col // 3]
                if sqr.value == 2:
                    v = sqr.squares[row % 3][col % 3]
                    if v == PLAYER_X:
                        out[row + row // 3][2 * col] = 'X'
                    if v == PLAYER_O:
                        out[row + row // 3][2 * col] = 'O'

        for i in range(11):
            out[i][5] = '#'
            out[i][11] = '#'

        return "\n".join(map(lambda t: "".join(t), out))

    def deepcopy(self):
        """
        copy current board
        :return: new Board with current data
        """
        return copy.deepcopy(self)

    def create_ultimate(self):
        """
        Create ultimate tictactoe
        :return:
        """
        for row in range(DIM):
            for col in range(DIM):
                margin = self.margin - 7
                size = self.dims.sqsize - 2 * margin
                xcor = self.dims.xcor + (col * self.dims.sqsize) + margin
                ycor = self.dims.ycor + (row * self.dims.sqsize) + margin
                dims = BoardDim(size=size, base_size=self.dims.sqsize, xcor=xcor, ycor=ycor)

                linewidth = self.linewidth - 7
                self.squares[row][col] = Board(dims=dims, linewidth=linewidth, margin=margin + self.margin, sub=True)

    def valid_sqr(self, col, row):
        """
        Check sqr is valid?
        :param col: current col
        :param row: current row
        :return: True if sqr is valid else False
        """
        if col == -1 or row == -1:
            return False

        main_row = row // 3
        main_col = col // 3

        sub_row = row % 3
        sub_col = col % 3

        valid_col = self.valid_col
        valid_row = self.valid_row

        if self.squares[valid_row][valid_col].value == 2:
            if main_row != valid_row or main_col != valid_col:
                return False

        sqr = self.squares[main_row][main_col].squares[sub_row][sub_col]

        if not sqr == 2:
            return False

        return True

    def get_valids(self):
        """
        search list of valid position
        :return: list valids position
        """
        list_valid_sqrs = []

        for r in range(9):
            for c in range(9):
                if self.valid_sqr(r, c):
                    list_valid_sqrs.append((r, c))

        return list_valid_sqrs

    def mark_sqr(self, col, row, player):
        """
        mark player in square
        :param col: current col
        :param row: current row
        :param player: current player
        :return:
        """
        main_row = row // 3
        main_col = col // 3

        sub_row = row % 3
        sub_col = col % 3

        self.squares[main_row][main_col].squares[sub_row][sub_col] = player

    def check_win(self, matrix):
        """
        check board status
        :return:
        1: player X win
        -1: player O win
        0: draw
        2: don't finish
        """
        # Vertical win
        for col in range(DIM):
            if matrix[0][col] == matrix[1][col] == matrix[2][col] != 2:
                return matrix[0][col]

        # Horizontal win
        for row in range(DIM):
            if matrix[row][0] == matrix[row][1] == matrix[row][2] != 2:
                return matrix[row][0]

        # Diagonal win
        # Desc
        if matrix[0][0] == matrix[1][1] == matrix[2][2] != 2:
            return matrix[1][1]

        # Asc
        if matrix[0][2] == matrix[1][1] == matrix[2][0] != 2:
            return matrix[1][1]

        for row in range(DIM):
            for col in range(DIM):
                if matrix[row][col] == 2:
                    return 2

        return 0
