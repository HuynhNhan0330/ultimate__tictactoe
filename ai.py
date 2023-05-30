import random
import math

from const import *


class AI:
    def __init__(self, level=0, player=-1):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_valids()
        index = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[index]

    def eval(self, board):
        if self.level == 0:
            move = self.rnd(board)
        else:
            minimaxap = Minimaxap(board)
            move = minimaxap.search(board, 3, -math.inf, math.inf, self.player, True)[1]

        return move


class Minimaxap():
    def __init__(self, board):
        self.board = board

    def search(self, board, depth, alpha, beta, player, isMaximizer):
        matrix = []
        for r in range(DIM):
            m = []
            for c in range(DIM):
                m.append(board.squares[r][c].value)
            matrix.append(m)

        if depth == 0 or not board.check_win(matrix) == 2:
            return self.evaluate(board, player), None

        pos = None
        list_valid_move = board.get_valids()

        if isMaximizer:
            maxEval = -math.inf

            for r, c in list_valid_move:
                copyBoard = board.deepcopy()
                value = self.search(copyBoard, depth - 1, alpha, beta, -player, False)[0]

                if value > maxEval:
                    maxEval = value
                    pos = (r, c)

                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            return maxEval, pos

        else:
            minEval = math.inf

            for r, c in list_valid_move:
                copyBoard = board.deepcopy()
                value = self.search(copyBoard, depth - 1, alpha, beta, -player, True)[0]

                if minEval > value:
                    minEval = value
                    pos = (r, c)

                beta = min(beta, value)
                if beta <= alpha:
                    break

            return minEval, pos

    def evaluate(self, board, player):
        score = 0
        for r in range(DIM):
            for c in range(DIM):
                if board.squares[r][c].value == 2:
                    score += self.evaluate_sub_board(board.squares[r][c].squares, player)

        return score

    def evaluate_sub_board(self, matrix, player):
        score = 0

        # Score row
        for row in matrix:
            score += self.count_score(row, player)

        # Score column
        for col in range(3):
            cols = []
            for row in range(3):
                cols.append(matrix[row][col])

            score += self.count_score(cols, player)

        # Score diagonal
        # asc
        diags = []
        for indx in range(len(matrix)):
            diags.append(matrix[indx][indx])

        score += self.count_score(diags, player)

        # desc
        diags_2 = []
        for indx, rev_indx in enumerate(reversed(range(len(matrix)))):
            diags_2.append(matrix[indx][rev_indx])
        score += self.count_score(diags_2, player)

        if self.board.check_win(matrix) == 0:
            score += 1

        return score

    def count_score(self, array, player):
        opp_player = -player
        score = 0

        if array.count(player) == 3:
            score += 100

        elif array.count(player) == 2:
            score += 50

        elif array.count(player) == 1:
            score += 20

        if array.count(opp_player) == 3:
            score -= 100

        elif array.count(opp_player) == 2:
            score -= 50

        if array.count(player) == 1 and array.count(opp_player) == 2:
            score += 10

        return score
