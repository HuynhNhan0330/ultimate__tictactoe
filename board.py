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

        sqr = self.squares[main_row][main_col]
        if not sqr.value == 2:
            return False

        if not sqr.squares[sub_row][sub_col] == 2:
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
                if self.valid_sqr(c, r):
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
        self.set_win(col, row)

    def set_win(self, col, row):
        """
        set value win
        :param col: current column
        :param row: current row
        :return:
        """
        main_row = row // 3
        main_col = col // 3
        sqr = self.squares[main_row][main_col]

        matrix = []
        for r in range(DIM):
            m = []
            for c in range(DIM):
                m.append(sqr.squares[r][c])
            matrix.append(m)

        is_check_winner = self.check_win(matrix)
        if not is_check_winner == 2:
            self.squares[main_row][main_col].value = is_check_winner

        matrix = []
        for r in range(DIM):
            m = []
            for c in range(DIM):
                m.append(self.squares[r][c].value)
            matrix.append(m)

        is_check_winner = self.check_win(matrix)
        if not is_check_winner == 2:
            self.value = is_check_winner

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
            if matrix[0][col] != 0 and matrix[0][col] == matrix[1][col] == matrix[2][col] != 2:
                return matrix[0][col]

        # Horizontal win
        for row in range(DIM):
            if matrix[row][0] != 0 and matrix[row][0] == matrix[row][1] == matrix[row][2] != 2:
                return matrix[row][0]

        # Diagonal win
        # Desc
        if matrix[1][1] != 0 and matrix[0][0] == matrix[1][1] == matrix[2][2] != 2:
            return matrix[1][1]

        # Asc
        if matrix[1][1] != 0 and matrix[0][2] == matrix[1][1] == matrix[2][0] != 2:
            return matrix[1][1]

        for row in range(DIM):
            for col in range(DIM):
                if matrix[row][col] == 2:
                    return 2

        return 0

    def get_main_board(self):
        """
        get main board in ultimate board
        :return: matrix
        """
        matrix = [[0, 0, 0] for row in range(DIM)]
        for r in range(DIM):
            for c in range(DIM):
                matrix[r][c] = self.squares[r][c].value

        return matrix

    def get_score_flags(self, board):
        """
        get score flags
        :param board: current board
        :return: score flags with datatypes dictionary
        """
        score_flags = {-1: 0, 0: 0, 1: 0, 2: 0}
        for r in range(3):
            for c in range(3):
                score_flags[board[r][c]] += 1
        return score_flags
